"""Sdílené stavební prvky pro stránky v jednotném designu (globální barvy/písma sbz_*, design/design-system.json).

Použití ve stavebním skriptu:  from sbz import *;  load("post-XXXX.json", prefix="sbz-xxx")
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UP = "https://sandbox.xafour.eu/wp-content/uploads/"
KONTAKT = "/kontakt-s-blankou-za-hranice/"
OBJEDNAT_PODPORU = "https://form.simpleshop.cz/4zRXn/buy/"
OBJEDNAT_PRUVODCE = "https://form.simpleshop.cz/AaExm/buy/"
TELEFON = "tel:+420777060809"
PREFIX = "sbz"

_n = 0


def eid():
    global _n
    _n += 1
    return hashlib.md5(f"{PREFIX}-{_n}".encode()).hexdigest()[:7]


def g(kind, id_):
    return f"globals/{kind}?id={id_}"


# ---------- obsah z původní stránky ----------
images = {}
testimonials = []


def _walk(els):
    for e in els:
        s = e.get("settings", {})
        for v in s.values():
            if isinstance(v, dict) and v.get("id") and str(v.get("url", "")).lower().endswith((".jpg", ".jpeg", ".png")):
                images[v["url"].split("/uploads/")[-1]] = v["id"]
        if e.get("widgetType") == "testimonial":
            img = s.get("testimonial_image") or {}
            testimonials.append({
                "content": s.get("testimonial_content", ""),
                "name": s.get("testimonial_name", ""),
                "job": s.get("testimonial_job", ""),
                "image": {"id": img.get("id"), "url": img.get("url")} if img.get("id") else None,
            })
        _walk(e.get("elements", []))




def load(*snapshot_names, prefix):
    """Načte texty/fotky/reference z exportů stránek a nastaví prefix pro id prvků."""
    global PREFIX, _n
    PREFIX, _n = prefix, 0
    for name in snapshot_names:
        _walk(json.loads((ROOT / "snapshots" / name).read_text())["meta"]["_elementor_data"])


def img(path):
    return {"id": images[path], "url": UP + path, "size": "", "alt": "", "source": "library"}


def clean_html(s):
    """Text z editoru bez ručních stylů (barvy, písma, velikosti)."""
    s = re.sub(r'\s(style|class|data-[\w-]+)="[^"]*"', "", s)
    s = re.sub(r"</?span>", "", s)
    s = re.sub(r"</?font[^>]*>", "", s)
    s = s.replace("https://sandbox.xafour.eu/kontakt", KONTAKT.rstrip("/"))
    return s.strip()


# ---------- stavební prvky ----------
def heading(title, level="h2", typo=None, color="sbz_zelena", align="left", css=""):
    typo = typo or {"h1": "sbz_h1", "h2": "sbz_h2", "h3": "sbz_h3"}.get(level, "sbz_h3")
    return {"id": eid(), "elType": "widget", "widgetType": "heading", "elements": [], "settings": {
        "title": title, "header_size": level, "align": align, "_css_classes": css,
        "__globals__": {"typography_typography": g("typography", typo), "title_color": g("colors", color)}}}


def eyebrow(text, align="left", color="sbz_oliva"):
    return heading(text, "p", "sbz_nadtitulek", color, align)


def text(html_, align="left", color="sbz_text", typo="sbz_text", css="sbz-text"):
    return {"id": eid(), "elType": "widget", "widgetType": "text-editor", "elements": [], "settings": {
        "editor": html_, "align": align, "_css_classes": css,
        "__globals__": {"typography_typography": g("typography", typo), "text_color": g("colors", color)}}}


def button(label, url, style="primary", align="left", inline=False):
    """Jednotná tlačítka na celém webu (přání Blanky 15. 10.: žádné změny barvy po najetí myší).
    primary = plné tmavě zelené, po najetí jen o odstín tmavší (CSS .sbz-btn);
    secondary = bílé se zeleným obrysem, po najetí světle olivové – je vidět na fotce i na barevném pozadí.
    Staré styly "light"/"outline-light" (pro tmavé sekce) už nejsou, tmavé sekce na webu nebudou."""
    style = {"light": "primary", "outline-light": "secondary"}.get(style, style)
    s = {"text": label, "link": {"url": url, "is_external": "on" if url.startswith("http") else "", "nofollow": ""},
         "align": align, "size": "md", "_css_classes": "sbz-btn sbz-btn-" + style,
         "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True},
         "border_border": "solid",
         "border_width": {"unit": "px", "top": "2", "right": "2", "bottom": "2", "left": "2", "isLinked": True},
         "text_padding": {"unit": "px", "top": "14", "right": "28", "bottom": "14", "left": "28", "isLinked": False},
         "__globals__": {"typography_typography": g("typography", "sbz_tlacitko")}}
    G = s["__globals__"]
    G.update(border_color=g("colors", "sbz_zelena"), button_hover_border_color=g("colors", "sbz_zelena"))
    if style == "primary":
        G.update(background_color=g("colors", "sbz_zelena"), button_text_color=g("colors", "sbz_bila"),
                 button_background_hover_color=g("colors", "sbz_zelena"), hover_color=g("colors", "sbz_bila"))
    else:
        G.update(background_color=g("colors", "sbz_bila"), button_text_color=g("colors", "sbz_zelena"),
                 button_background_hover_color=g("colors", "sbz_louka"), hover_color=g("colors", "sbz_zelena"))
    if inline:
        s["_element_width"] = "auto"
        s["_margin"] = {"unit": "px", "top": "0", "right": "12", "bottom": "12", "left": "0", "isLinked": False}
    return {"id": eid(), "elType": "widget", "widgetType": "button", "elements": [], "settings": s}


def icon_list(items, icon="fas fa-check", color="sbz_text", icon_color="sbz_oliva"):
    return {"id": eid(), "elType": "widget", "widgetType": "icon-list", "elements": [], "settings": {
        "icon_list": [{"_id": eid(), "text": t, "selected_icon": {"value": icon, "library": "fa-solid"}} for t in items],
        "space_between": {"unit": "px", "size": 12, "sizes": []},
        "icon_size": {"unit": "px", "size": 16, "sizes": []},
        "icon_self_align": "left", "icon_self_vertical_align": "flex-start",
        "icon_vertical_offset": {"unit": "px", "size": 4, "sizes": []},
        "text_indent": {"unit": "px", "size": 10, "sizes": []},
        "__globals__": {"icon_color": g("colors", icon_color), "text_color": g("colors", color),
                        "icon_typography_typography": g("typography", "sbz_text")}}}


def image(path, caption="", css="sbz-foto", link=None):
    s = {"image": img(path), "image_size": "large", "_css_classes": css, "align": "center"}
    if caption:
        s.update(caption_source="custom", caption=caption)
    if link:
        s.update(link_to="custom", link={"url": link, "is_external": "", "nofollow": ""})
    return {"id": eid(), "elType": "widget", "widgetType": "image", "elements": [], "settings": s}


def icon_box(icon, title, desc=""):
    return {"id": eid(), "elType": "widget", "widgetType": "icon-box", "elements": [], "settings": {
        "selected_icon": {"value": icon, "library": "fa-solid"}, "title_text": title, "description_text": desc,
        "title_size": "h3", "view": "stacked", "shape": "circle", "position": "top",
        "icon_size": {"unit": "px", "size": 26, "sizes": []}, "icon_padding": {"unit": "px", "size": 18, "sizes": []},
        "_css_classes": "sbz-karta",
        "__globals__": {"primary_color": g("colors", "sbz_svetla"), "secondary_color": g("colors", "sbz_zelena"),
                        "title_typography_typography": g("typography", "sbz_h3"), "title_color": g("colors", "sbz_zelena"),
                        "description_typography_typography": g("typography", "sbz_text"),
                        "description_color": g("colors", "sbz_text")}}}


def testimonial(t):
    s = {"testimonial_content": re.sub(r"\s*\n\s*\n\s*", "<br><br>", t["content"].strip()).replace("\n", "<br>"), "testimonial_name": t["name"], "testimonial_job": t["job"],
         "testimonial_alignment": "left", "testimonial_image_position": "top", "_css_classes": "sbz-karta sbz-reference",
         "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "24", "left": "0", "isLinked": False},
         "__globals__": {"content_typography_typography": g("typography", "sbz_text"),
                         "content_content_color": g("colors", "sbz_text"),
                         "name_typography_typography": g("typography", "sbz_tlacitko"),
                         "name_text_color": g("colors", "sbz_zelena"),
                         "job_typography_typography": g("typography", "sbz_maly"),
                         "job_text_color": g("colors", "sbz_seda")}}
    if t["image"]:
        s["testimonial_image"] = {**t["image"], "size": "", "alt": t["name"], "source": "library"}
        s["testimonial_image_size"] = "thumbnail"
    return {"id": eid(), "elType": "widget", "widgetType": "testimonial", "elements": [], "settings": s}


def column(widgets, size=100, css="", align="", valign="", mobile=None):
    s = {"_column_size": int(size), "_inline_size": None if size == 100 else size, "css_classes": css}
    if mobile:
        s["_inline_size_mobile"] = mobile
    if align:
        s["align"] = align
    if valign:
        s["content_position"] = valign
    return {"id": eid(), "elType": "column", "isInner": False, "settings": s, "elements": widgets}


def section(columns, bg=None, pad=88, pad_m=56, gap="extended", width=1140, anchor="", extra=None, valign=""):
    s = {"layout": "boxed", "content_width": {"unit": "px", "size": width, "sizes": []}, "gap": gap,
         "padding": {"unit": "px", "top": str(pad), "right": "24", "bottom": str(pad), "left": "24", "isLinked": False},
         "padding_mobile": {"unit": "px", "top": str(pad_m), "right": "16", "bottom": str(pad_m), "left": "16", "isLinked": False},
         "__globals__": {}}
    bg = bg or "sbz_bila"  # bez barvy by sekce převzala krémové pozadí šablony
    s["background_background"] = "classic"
    s["__globals__"]["background_color"] = g("colors", bg)
    if anchor:
        s["_element_id"] = anchor
    if valign:
        s["content_position"] = valign
    if extra:
        s.update(extra)
    return {"id": eid(), "elType": "section", "isInner": False, "settings": s, "elements": columns}


def hl(before, mark, after=""):
    return f'{before}<span class="sbz-hl">{mark}</span>{after}'




# Úvodní fotka stránky (hero). Styly k výběru:
#   "pulka"   – text vlevo na světle olivovém pozadí, fotka vpravo ostrá a celá vidět, bez závoje (návrh 15. 10.)
#   "zelena"  – tmavě zelený závoj, bílý text (první návrh, Blanka nechce)
#   "krem"    – světlý krémový závoj, zelený text
#   "broskev" – závoj ve světlé doplňkové barvě, zelený text
#   "oliva"   – světle olivový závoj (jako lišta cookies / dnešní web), zelený text
#   "karta"   – fotka bez závoje, text v krémové kartě uprostřed
UVOD_ZAVOJ = {"zelena": ("sbz_zelena", 0.62), "krem": ("sbz_krem", 0.74), "broskev": ("sbz_svetla", 0.70),
              "oliva": ("#E6EBC0", 0.74)}


def hero(nadtitulek, nadpis, popis_html, tlacitka, obrazek, styl="pulka", vyska=560):
    """tlacitka = [(text, url), ...] – první je hlavní, druhé obrysové."""
    if styl == "pulka":
        # Fotka jako obrázek (ne pozadí): neořízne se, nezvětšuje se nad svou velikost, a proto zůstane ostrá.
        w = [eyebrow(nadtitulek), heading(nadpis, "h1"), text(popis_html)]
        w += [button(t, u, "primary" if i == 0 else "secondary", inline=True) for i, (t, u) in enumerate(tlacitka)]
        foto = image(obrazek, css="sbz-uvod-foto")
        foto["settings"]["image_size"] = "full"
        return section([column(w, 48, valign="middle"),
                        column([foto], 52, valign="middle")],
                       bg="sbz_louka", pad=64, pad_m=40, width=1200, valign="middle",
                       extra={"css_classes": "sbz-uvod sbz-uvod-pulka", "reverse_order_mobile": "reverse-mobile"})
    tmavy = styl == "zelena"
    w = [eyebrow(nadtitulek, "center", "sbz_svetla" if tmavy else "sbz_oliva"),
         heading(nadpis, "h1", color="sbz_bila" if tmavy else "sbz_zelena", align="center"),
         text(popis_html, "center", "sbz_bila" if tmavy else "sbz_text")]
    for i, (t, u) in enumerate(tlacitka):
        w.append(button(t, u, ("light" if i == 0 else "outline-light") if tmavy else ("primary" if i == 0 else "secondary"),
                        inline=True))
    extra = {"height": "min-height", "custom_height": {"unit": "px", "size": vyska, "sizes": []},
             "custom_height_mobile": {"unit": "px", "size": 480, "sizes": []},
             "background_background": "classic", "background_image": img(obrazek),
             "background_position": "center center", "background_size": "cover", "background_repeat": "no-repeat",
             "css_classes": "sbz-uvod sbz-uvod-" + styl}
    if styl in UVOD_ZAVOJ:
        barva, kryti = UVOD_ZAVOJ[styl]
        extra.update({"background_overlay_background": "classic",
                      "background_overlay_opacity": {"unit": "px", "size": kryti, "sizes": []}})
        if barva.startswith("#"):
            extra["background_overlay_color"] = barva
        else:
            extra["__globals__"] = {"background_overlay_color": g("colors", barva)}
    col = column(w, align="center", css="sbz-uvod-karta" if styl == "karta" else "")
    return section([col], pad=120 if styl != "karta" else 96, pad_m=72 if styl != "karta" else 40,
                   width=1140 if styl != "karta" else 800, extra=extra, valign="middle")
