#!/usr/bin/env python3
"""Rozloží export webu (JSON z tools/server/export-all.php) do složky web/.

Každá stránka/článek/šablona = jeden soubor, aby git ukazoval změny po řádcích:
  web/stranky/<slug>.json     – kompletní data stránky (Elementor JSON)
  web/texty/<slug>.md         – jen čitelné texty stránky (pro snadné porovnání změn textu)
  web/clanky/, web/sablony/   – totéž pro články a šablony Elementoru
  web/nastaveni/              – menu, pluginy, vlastní CSS, nastavení šablony Kadence

Do veřejného repa jdou jen publikované věci; soukromé adresy z nastavení formulářů se maskují.

Použití: python3 tools/export_web.py export-all.json [--bez-redesignu]
  --bez-redesignu  vynechá kopie *-novy-design, globální styly sbz_* a CSS blok sbz (= stav před redesignem)
"""
import html
import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
SKRYT = {"bstul@seznam.cz": "skryty-email@example.invalid"}  # cílové adresy formulářů (na webu nejsou vidět)
ŽIVÝ = "https://sblankouzahranice.eu"
SANDBOX = "https://sandbox.xafour.eu"
ZAHODIT_META = {"_elementor_css", "_elementor_controls_usage", "_elementor_page_assets", "_elementor_element_cache",
                "_elementor_version", "_elementor_pro_version", "_elementor_screenshot"}
TEXT_KLICE = {"title", "editor", "text", "before_text", "highlighted_text", "rotating_text", "after_text",
              "description_text", "title_text", "testimonial_content", "testimonial_name", "testimonial_job",
              "tab_title", "tab_content", "item_description", "button_text", "heading", "description", "content",
              "caption", "field_label", "placeholder", "submit_button_text", "alert_title", "alert_description",
              "inner_text", "prefix", "suffix", "ending_number"}
CSS_BLOK = re.compile(r"/\* =+ BEGIN sbz design system.*?END sbz design system =+ \*/\n?", re.S)


class Text(HTMLParser):
    BLOK = {"p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "tr"}

    def __init__(self):
        super().__init__()
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOK:
            self.out.append("\n")
        if tag == "li":
            self.out.append("- ")

    def handle_data(self, data):
        self.out.append(data)


def text_z_html(s):
    if not isinstance(s, str):
        return ""
    p = Text()
    p.feed(s)
    t = html.unescape("".join(p.out)).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    return "\n".join(r.strip() for r in t.splitlines() if r.strip())


def texty_settings(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in TEXT_KLICE and isinstance(v, str) and v.strip() and not v.startswith(("http", "#", "{")):
                out.append(text_z_html(v))
            elif isinstance(v, (list, dict)):
                texty_settings(v, out)
    elif isinstance(o, list):
        for v in o:
            texty_settings(v, out)


def texty_elementor(elements, out):
    for el in elements or []:
        w = el.get("widgetType")
        s = el.get("settings", {})
        if w == "heading":
            out.append("## " + text_z_html(s.get("title", "")))
        elif w == "image" and isinstance(s.get("image"), dict):
            out.append("[obrázek: %s]" % s["image"].get("url", "").rsplit("/", 1)[-1])
        elif w:
            texty_settings(s, out)
        texty_elementor(el.get("elements"), out)


def maskuj(o):
    s = json.dumps(o, ensure_ascii=False)
    for a, b in SKRYT.items():
        s = s.replace(a, b)
    return json.loads(s)


def na_zivy_web(o):
    """Sandbox je kopie živého webu (import přepsal doménu) – v exportu vracíme skutečnou adresu."""
    if isinstance(o, str):
        return o.replace("http://sandbox.xafour.eu", ŽIVÝ).replace("https://sandbox.xafour.eu", ŽIVÝ) \
                .replace("@sandbox.xafour.eu", "@sblankouzahranice.eu")
    if isinstance(o, list):
        return [na_zivy_web(v) for v in o]
    if isinstance(o, dict):
        return {k: na_zivy_web(v) for k, v in o.items()}
    return o


def bez_redesignu_kit(meta):
    ps = meta.get("_elementor_page_settings")
    if isinstance(ps, dict):
        for k in ("system_colors", "custom_colors", "system_typography", "custom_typography"):
            if isinstance(ps.get(k), list):
                ps[k] = [g for g in ps[k] if not str(g.get("_id", "")).startswith("sbz_")]


def zapis(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data if data.endswith("\n") else data + "\n")
    else:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def main():
    src = Path(sys.argv[1])
    puvodni = "--bez-redesignu" in sys.argv
    d = maskuj(json.loads(src.read_text()))
    for sub in ("stranky", "clanky", "sablony", "texty", "nastaveni"):
        shutil.rmtree(WEB / sub, ignore_errors=True)
    rows = []
    slozka = {"page": "stranky", "post": "clanky", "elementor_library": "sablony"}
    for p in d["posts"]:
        if p["status"] != "publish" or p["has_password"] or p["type"] not in slozka:
            continue
        if puvodni and p["slug"].endswith("-novy-design"):
            continue
        meta = {k: v for k, v in p["meta"].items() if k not in ZAHODIT_META}
        if isinstance(meta.get("_elementor_data"), str):
            try:
                meta["_elementor_data"] = json.loads(meta["_elementor_data"])
            except ValueError:
                pass
        meta = na_zivy_web(meta)
        p = na_zivy_web(p)
        if puvodni and meta.get("_elementor_template_type") == "kit":
            bez_redesignu_kit(meta)
        if p["slug"].endswith("-novy-design"):  # kopie v novém designu existují jen na sandboxu
            p["link"] = p["link"].replace(ŽIVÝ, SANDBOX)
        jmeno = p["slug"] or str(p["ID"])
        if p["type"] == "post":
            jmeno = p["date"][:4] + "-" + jmeno
        sl = slozka[p["type"]]
        zaznam = {k: p[k] for k in ("ID", "type", "title", "slug", "parent", "date", "modified", "excerpt",
                                     "categories", "link")}
        zaznam["obsah_wordpress"] = p["content"]
        zaznam["meta"] = meta
        zapis(WEB / sl / (jmeno + ".json"), zaznam)
        out = ["# " + html.unescape(p["title"]), "", "Adresa: " + p["link"], ""]
        el = meta.get("_elementor_data")
        if isinstance(el, list) and el:
            texty_elementor(el, out)
        else:
            out.append(text_z_html(p["content"]))
        popis = meta.get("_yoast_wpseo_metadesc")
        if popis:
            out[3:3] = ["Popis pro Google: " + popis, ""]
        zapis(WEB / "texty" / sl / (jmeno + ".md"), re.sub(r"\n{3,}", "\n\n", "\n\n".join(x for x in out if x)))
        rows.append((sl, jmeno, html.unescape(p["title"]), p["link"]))
    d = na_zivy_web(d)
    css = d.get("custom_css", "")
    if puvodni:
        css = CSS_BLOK.sub("", css)
    zapis(WEB / "nastaveni" / "vlastni-css.css", css)
    zapis(WEB / "nastaveni" / "menu.json", d["menus"])
    zapis(WEB / "nastaveni" / "pluginy.json", d["plugins"])
    mods = {k: v for k, v in d["theme_mods"].items() if k not in ("custom_css_post_id",)}
    zapis(WEB / "nastaveni" / "sablona-kadence.json", mods)
    zapis(WEB / "nastaveni" / "web.json", dict(d["settings"], wp_version=d["wp_version"], theme=d["theme"]))
    nazvy = {"stranky": "Stránky", "clanky": "Články", "sablony": "Šablony Elementoru (hlavička, patička, sekce)"}
    md = ["# Obsah webu sblankouzahranice.eu", "",
          "Automatický export (`tools/export_web.py`). U každé položky je kompletní data (`.json`) "
          "a čitelný text (`texty/…md`) – na GitHubu tak jde u každé změny vidět, co přesně se změnilo.", ""]
    for sl in ("stranky", "clanky", "sablony"):
        md += ["## " + nazvy[sl], "", "| Název | Data | Text |", "|---|---|---|"]
        for s, j, t, link in sorted((r for r in rows if r[0] == sl), key=lambda r: r[2].lower()):
            t = t.replace("|", "/") or "(bez názvu)"
            md.append(f"| [{t}]({link}) | [json]({sl}/{j}.json) | [text](texty/{sl}/{j}.md) |")
        md.append("")
    zapis(WEB / "README.md", "\n".join(md))
    print(len(rows), "položek ->", WEB)


if __name__ == "__main__":
    main()
