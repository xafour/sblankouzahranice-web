#!/usr/bin/env python3
"""Změny textů na nových stránkách jako Wordový dokument ke schválení (stejný vzhled jako SEO dokument).

Data: tools/texty/<stránka>.json z tools/texty/porovnej.py (stará stránka na živém webu × nová na sandboxu).
Použití: python3 tools/texty_docx.py [navrhy/TEXTY-ke-schvaleni.docx]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from seo_docx import Cm, Document, Pt, WD_ORIENT, nadpis, odstavec, qn, tabulka  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "navrhy/TEXTY-ke-schvaleni.docx"
DIR = os.path.join(os.path.dirname(__file__), "texty")
STRANKY = [
    ("Den ve Vídni", "den-ve-vidni", "https://sblankouzahranice.eu/den-ve-vidni/",
     "https://sandbox.xafour.eu/den-ve-vidni-novy-design/"),
    ("Vídeň – individuální cestovní podpora", "viden-podpora", "https://sblankouzahranice.eu/viden-cestovni-podpora/",
     "https://sandbox.xafour.eu/viden-cestovni-podpora-novy-design/"),
]
OTAZKY = [
    "Obě stránky: věta „Vídeň nabízí tolik krásných míst a zážitků, že bez místního průvodce snadno minete to nejlepší“ "
    "je z vaší původní stránky, ale slovo „průvodce“ tu znamená osobu. Navrhuji „bez někoho místního snadno minete to "
    "nejlepší“. Souhlasíte, nebo napište jiné znění.",
]


def main():
    doc = Document()
    s = doc.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    for okraj in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, okraj, Cm(1.5))
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    nadpis(doc, "Texty na nových stránkách – ke schválení", 0)
    odstavec(doc, "Připraveno 16. 10. 2026. Texty jsem nepsal znovu, jen jsem je učesal: opravil překlepy, velká písmena "
             "uprostřed vět nahradil běžnými, zkrátil dlouhé věty a doplnil krátké nadpisy a tlačítka, které nová stránka potřebovala.")
    nadpis(doc, "Jak dokument vyplnit")
    for t, txt in [
        ("Nový text je v pořádku: ", "klikněte na políčko ☐ ve sloupci Souhlasím (změní se na ☒)."),
        ("Chcete jiný text: ", "napište ho do sloupce Vaše změna. Můžete napsat i „vrátit původní“."),
        ("Hotovo: ", "dokument uložte do složky Dokumenty a napište mi. Vše pak upravím na zkušebním webu najednou."),
    ]:
        odstavec(doc, txt, t).style = "List Bullet"
    odstavec(doc, "Šedá poznámka u textu říká, o jakou změnu jde. „Jen velká písmena“ znamená, že slova zůstala stejná "
             "a změnilo se jen psaní velkými písmeny nebo interpunkce.")

    nadpis(doc, "Otázka k oběma stránkám")
    tabulka(doc, ["Otázka"], [17.0], [[q] for q in OTAZKY], souhlas=False)

    for c, (nazev, klic, stara, nova) in enumerate(STRANKY, 1):
        d = json.load(open(os.path.join(DIR, klic + ".json"), encoding="utf-8"))
        nadpis(doc, f"{c}. {nazev}")
        odstavec(doc, f"Původní stránka: {stara}\nNová stránka: {nova}")
        radky = []
        for r in d["radky"]:
            pozn = "jen velká písmena" if r["jen_pismena"] else ("nový nadpis / tlačítko" if not r["puvodne"] else "")
            radky.append([(r["nove"], pozn) if pozn else r["nove"], r["puvodne"] or "–"])
        tabulka(doc, ["Nově", "Původně"], [8.5, 8.5], radky)
        if d["vypustene"]:
            nadpis(doc, f"{c}a. {nazev}: texty, které na nové stránce nejsou", 2)
            odstavec(doc, "Většinou je nahradil formulář nebo tlačítko. Souhlasím = může zůstat vynechané; "
                     "do sloupce Vaše změna napište, kam text vrátit.")
            tabulka(doc, ["Původní text"], [17.0], [[v] for v in d["vypustene"]])

    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
