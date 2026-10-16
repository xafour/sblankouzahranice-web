#!/usr/bin/env python3
"""Přečte Blančin vyplněný dokument SEO-NAVRHY-ke-schvaleni (.odt) a udělá z něj seznam schválených textů (JSON).
☒ = můj návrh, vyplněný sloupec Vaše změna = její text, „NE“ = vynechat.
Použití: python3 -I tools/seo/odt2json.py vyplneno.odt > tools/seo/schvaleno.json"""
import json, re, sys, zipfile
import xml.etree.ElementTree as ET

T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
root = ET.fromstring(zipfile.ZipFile(sys.argv[1]).read("content.xml"))
txt = lambda e: " ".join("".join(e.itertext()).split())
tabulky = [[[txt(c) for c in r.findall(T + "table-cell")] for r in t.iter(T + "table-row")][1:] for t in root.iter(T + "table")]
bez_zn = lambda s: re.sub(r"\s*\(\d+ zn\.\)$", "", s)
# zjevné překlepy v dokumentu (opravené po domluvě)
OPRAVY = {"jistoru": "jistotu"}


def vyber(navrh, souhlas, zmena):
    if zmena.upper().startswith("NE"):
        return None
    if zmena:
        for a, b in OPRAVY.items():
            zmena = zmena.replace(a, b)
        return zmena
    return bez_zn(navrh) if "☒" in souhlas else None


out = {"titulky": {}, "popisy": {}, "skryt": [], "alt": {}, "poznamky": []}
stranka = None
for r in tabulky[0]:
    stranka = r[0] or stranka
    v = vyber(r[2], r[3], r[4])
    if v:
        out["titulky" if r[1] == "SEO titulek" else "popisy"][stranka] = v
for r in tabulky[1]:
    if r[3].upper().startswith("NE"):
        out["skryt"].append(r[0]); out["poznamky"].append(f"{r[0]}: {r[3]}")
        continue
    v = vyber(r[1], r[2], r[3])
    if v:
        out["popisy"][r[0]] = v
for r in tabulky[2]:
    if "☒" in r[2]:
        out["skryt"].append(r[0].split(",")[0])
    if r[3]:
        out["poznamky"].append(f"{r[0]}: {r[3]}")
for r in tabulky[3]:
    soubor, zmena = r[1], r[4]
    if "duplicitní" in zmena:  # „Stránka je duplicitní… Dej tam stejný text.Reference foto skupiny.“
        out["poznamky"].append(f"{r[0] or stranka}: {zmena}")
        zmena = zmena.rsplit("text.", 1)[-1].strip()
    v = vyber(r[2], r[3], zmena)
    klic = re.sub(r"(-\d+x\d+)?\.(png|jpe?g)$", "", soubor, flags=re.I)
    if v and klic not in out["alt"]:  # stejná fotka na více stránkách: popisek je u fotky jen jeden, platí první
        out["alt"][klic] = v.rstrip(".")
for r in tabulky[4]:
    out["poznamky"].append(f"{r[0][:70]}… → {r[1]}")
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
