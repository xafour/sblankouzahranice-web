"""Postaví novou verzi prodejní stránky „Den ve Vídni – váš plán do kapsy“ (on-line Průvodce do kapsy).

Vstup: snapshots/post-24571.json (+ post-19575.json kvůli id fotek). Formulář SimpleShop se přebírá beze změny.
Výstup: build/den-ve-vidni.json. Spuštění: python3 tools/build_den_ve_vidni.py
"""
import copy
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbz import *  # noqa: E402,F401,F403

load("post-24571.json", "post-19575.json", prefix="sbz-den")
SRC = json.loads((ROOT / "snapshots/post-24571.json").read_text())["meta"]["_elementor_data"]


def original_html_widgets():
    out = []

    def walk(els):
        for e in els:
            if e.get("widgetType") == "html" and (e.get("settings", {}).get("html") or "").strip():
                w = copy.deepcopy(e)
                w["id"] = eid()
                out.append(w)
            walk(e.get("elements", []))
    walk(SRC)
    return out


KOUPIT = OBJEDNAT_PRUVODCE
P = []

# 1) Úvod
P.append(hero("On-line průvodce do kapsy", "Den ve Vídni – váš průvodce do kapsy",
              "<p>Vídeň vlastním tempem, s pocitem podpory za zády. Nebloudíte, nehledáte a máte jistotu, že jdete správně a neztrácíte čas.</p>",
              [("Koupit průvodce", KOUPIT), ("Co průvodce obsahuje", "#obsah")],
              "2026/02/Zahlavi-new.jpg", os.environ.get("SBZ_UVOD", "pulka"), 540))

# 2) Co to je
P.append(section([
    column([
        eyebrow("Váš bod jistoty při objevování Vídně"),
        heading("Průvodce, který vás vede jasně, klidně a bez zbytečného zdržování"),
        text("<p><strong>Stejná trasa, kterou chodím s klienty, je nyní ve formě on-line produktu k okamžitému využití.</strong></p>"
             "<p>Vídeň nabízí tolik krásných míst a zážitků, že bez místního průvodce snadno minete to nejlepší. "
             "Jako Češka, žijící ve Vídni už 10 let, vám pomáhám poznat Vídeň snadněji a lehčeji – abyste ji poznali, a ne jen proběhli.</p>"),
        heading("On-line průvodce do kapsy obsahuje", "h3"),
        icon_list(["Itinerář trasy s popisem památek a turistických cílů.",
                   "Mapu ke stažení do mobilu pro snadnější orientaci.",
                   "Praktickou přílohu: přehled jízdenek a ticketů na městskou dopravu ve Vídni."]),
        text("<p>Vše komplet v jednom produktu. Vídeň objevujete pohodlně, vlastním tempem, ale tak, jako byste měli po celé trase můj osobní doprovod s výkladem.</p>"),
        button("Chci odzkoušenou trasu Vídní", KOUPIT, "primary"),
    ], 58, valign="middle"),
    column([image("2026/03/houpaci-kreslo.png", css="sbz-obrazek")], 42, valign="middle"),
], valign="middle"))

# 3) Možná to znáte
P.append(section([column([
    heading(hl("Možná to ", "znáte i vy"), align="center"),
    text("<p>Sice přesně víte, co všechno byste ve Vídni chtěli vidět, ale nemáte už tak přesnou představu, jak daleko od sebe památky jsou "
         "a jakou zvolit trasu nebo dopravu mezi jednotlivými cíli, abyste zbytečně neztráceli čas a nebloudili městem.</p>"
         "<p>Zkušenost mi ukazuje, že scénář představ o návštěvě Vídně je mnohdy hodně podobný. "
         "<strong>Teď je tu nástroj, který mnohé otázky a nejasnosti vyřeší.</strong></p>", "center"),
])], bg="sbz_svetla", width=820))

# 4) Pro koho
P.append(section([
    column([
        heading(hl("Průvodce je ", "pro vás", ", pokud")),
        icon_list([
            "Chcete jasně danou trasu širším centrem města a vidět nejdůležitější památky a cíle <strong>bez stresu a časových ztrát</strong>.",
            "<strong>Nepotřebujete osobní doprovod</strong> nebo nemáme společný volný termín.",
            "Chcete mít <strong>jistotu, že jdete „správně“</strong>.",
        ]),
    ], 58, valign="middle"),
    column([
        heading("Tohle není „jen“ PDF", "h3"),
        text("<p>Je to zkušenost a prověřená praxe. Pro vás pak: pohodlí, jistota, úspora času, žádný chaos a bod opory v kapse.</p>"),
    ], 42, css="sbz-karta", valign="middle"),
], valign="middle"))

# 5) Co přesně obsahuje
P.append(section([column([
    heading(hl("Co průvodce ", "přesně obsahuje")),
])], bg="sbz_svetla", anchor="obsah", extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "16", "left": "24", "isLinked": False}}))
P.append(section([
    column([icon_list([
        "<strong>Pěší trasu dlouhou 6 km širším centrem Vídně</strong>, na které uvidíte minimálně 10 nejdůležitějších památek a cílů.",
        "<strong>Podrobný itinerář trasy</strong> s popisem všech památek po cestě.",
        "<strong>Souvislosti, informace z historie a zajímavosti</strong>, které se mnozí turisté nedozví.",
        "<strong>QR kód a odkaz ke stažení mapy do mobilu</strong> pro pohodlnou orientaci na trase.",
    ])], 50),
    column([icon_list([
        "<strong>Přehlednou PDF verzi s fotografiemi</strong> připravenou k okamžitému použití.",
        "<strong>Přílohu: přehled jízdenek a ticketů</strong> na městskou dopravu ve Vídni včetně novinek platných od ledna 2026.",
        "<strong>Trasu, kterou zvládnou dospělí i děti</strong> v každém ročním období – osobně odzkoušeno.",
    ])], 50),
], bg="sbz_svetla", extra={"padding": {"unit": "px", "top": "16", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 6) Stejná trasa jako s klienty
P.append(section([
    column([image("2026/02/foto-moje-male.jpg", css="sbz-foto-vysoka")], 40, valign="middle"),
    column([
        heading("Stejnou trasou jako moji klienti – jen sami, s itinerářem v kapse"),
        text("<p>Projdete si Vídeň stejnou trasou, kterou chodím s klienty při osobním doprovodu, tentokrát sami, ale s mým podrobným itinerářem v kapse.</p>"
             "<p><strong>Přestaňte bloudit a začněte si metropoli užívat!</strong></p>"),
        button("Chci odzkoušenou trasu Vídní", KOUPIT, "primary"),
    ], 60, valign="middle"),
], valign="middle"))

# 7) Co vám přinese
P.append(section([
    column([
        heading(hl("Co vám průvodce ", "přinese")),
        icon_list([
            "Získáte odzkoušenou trasu městem a nezabloudíte mezi památkami.",
            "Za jeden půlden uvidíte z Vídně to podstatné bez chaosu a zbytečného přejíždění.",
            "Ke každé památce na trase budete mít informace.",
            "Projdete si Vídeň v pohodě, vlastním tempem, a sami rozhodnete, kde se zdržíte a co navštívíte.",
            "Po celou dobu budete mít pocit, že vás vede někdo místní.",
            "Budete vědět, jaký typ jízdenky na MHD si vybrat (novinky pro rok 2026 jsou v příloze).",
        ]),
    ], 58, valign="middle"),
    column([image("2026/02/20251015_164354.jpg", css="sbz-foto-vysoka")], 42, valign="middle"),
], bg="sbz_krem", valign="middle"))


# 8) Rozdíl oproti osobnímu doprovodu
def srovnani(path, title, desc, label, url, style):
    return column([image(path, css="sbz-foto"), heading(title, "h3"), text(f"<p>{desc}</p>"), button(label, url, style)],
                  50, css="sbz-karta")


P.append(section([column([
    heading(hl("Jaký je rozdíl oproti ", "osobnímu doprovodu", "?"), align="center"),
])], extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "24", "left": "24", "isLinked": False}}))
P.append(section([
    srovnani("2026/02/ja-u-Hundertwasserhaus-e1771793447643.jpg", "Osobní doprovod",
             "Individuální trasa na míru, možnost se na cokoliv zeptat a společná konverzace o životě v Rakousku. Nasměrování a rady na další cíle.",
             "Cestovní podpora na míru", "/viden-cestovni-podpora/", "secondary"),
    srovnani("2023/09/do-hlavicky2.jpg", "On-line průvodce",
             "Stejná trasa, stejné informace, jen bez mé přítomnosti a možnosti se doptat. Jednodušší a dostupnější varianta se stejnou kvalitou obsahu.",
             "Koupit průvodce", KOUPIT, "primary"),
], extra={"padding": {"unit": "px", "top": "8", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 9) Praktické informace (světle olivový pruh – dřív sytě zelený, Blance připadal agresivní)
P.append(section([
    column([
        heading("Praktické informace", "h2"),
        icon_list(["<strong>Délka trasy:</strong> cca 6 km.",
                   "<strong>Časová náročnost:</strong> 3–4 hodiny podle tempa, s návštěvou památek déle.",
                   "<strong>Start:</strong> Karlsplatz – 3 linky metra a zastávky několika linek tramvají i autobusů.",
                   "<strong>Stažení:</strong> ihned po zaplacení (PDF)."]),
    ], 58, valign="middle"),
    column([
        text("<p>Stále, i po skončení zaváděcí ceny, najdete příjemnou cenu za komplexnost celého produktu.</p>"),
        button("Chci průvodce ihned", KOUPIT, "primary"),
    ], 42, valign="middle"),
], bg="sbz_louka", pad=72, valign="middle"))

# 10) Kdo, co, proč
P.append(section([
    column([image("2026/02/Ja-u-Parlamentu.jpg", css="sbz-foto-vysoka")], 40),
    column([
        heading(hl("Kdo pro vás trasu ", "připravil")),
        heading("Kdo", "h3"),
        text("<p>Jmenuji se Blanka a ve Vídni žiji už několik let. Když jsem se v 50 letech přestěhovala z Prahy do Vídně, neuměla jsem ani slovo německy "
             "a každý den byl výzvou. Na začátku jsem se cítila podobně jako každý turista, který se ocitne v nové zemi, jejímž jazykem dobře nehovoří. "
             "Po pár letech ve Vídni vznikl můj projekt a nyní nabízím cestovní podporu – různé služby pro snadnější poznávání Vídně a okolí.</p>"),
        heading("Co", "h3"),
        text("<p>On-line průvodce (procházka Vídní) vznikl z osobní zkušenosti – z potřeby nabídnout vám rychlou a jednoduchou možnost osvědčené trasy, "
             "kterou se svými klienty procházím už roky, k okamžitému využití.</p>"),
        heading("Proč", "h3"),
        text("<p>V turistické sezoně se mi stalo, že se na mě obrátili klienti s poptávkou na stejný termín a já nemohla osobně vyhovět oběma. "
             "Nabídla jsem tedy projít trasu samostatně s předem připraveným itinerářem, podrobným popisem památek a mapkou do mobilu. "
             "Klient byl nadšený, a natolik spokojený, že se po roce do Vídně vrátil s celou rodinou a objednali si službu na míru.</p>"
             "<p><strong>Tak vznikl tento on-line průvodce – ne jako prvoplánová nabídka, ale jako nabídka, kterou si vyžádala praxe.</strong></p>"),
        button("Chci osvědčeného průvodce", KOUPIT, "primary"),
    ], 60),
], bg="sbz_svetla"))

# 11) Galerie trasy
gal = [("2023/05/Burggarten-1.jpg", "Burggarten"), ("2023/06/Fiakr2-S.jpg", "Typický vídeňský fiakr"),
       ("2023/06/Albertina.jpg", "Obrazárna Albertina"), ("2026/02/Hotel-Sacher.jpg", "Hotel Sacher"),
       ("2026/02/Budova-Secese.jpg", "Budova Secese"), ("2023/06/nocni.jpg", "Vídeňská opera"),
       ("2026/02/Hofburg-2.jpg", "Hofburg"), ("2026/02/Karlskirche.jpg", "Karlskirche"),
       ("2026/02/Kapucingrot.jpg", "Hrobka Habsburků"), ("2026/02/Znama-nakupni-trida.jpg", "Místa, kudy budete procházet"),
       ("2026/02/U-Albertiny.jpg", "Z procházky městem"), ("2026/02/Opera-z-vysky.jpg", "Vídeň jinak – snadněji, plynule a chytře"),
       ("2026/02/Fiakr-u-Albertina.jpg", "Fiakr u Albertiny"), ("2023/05/Sachr-2.jpg", "Originál Sacher dort"),
       ("2023/05/Hofburg-2.jpg", "Hofburg")]
P.append(section([column([
    heading(hl("Co na trase ", "uvidíte"), align="center"),
    text("<p>Obejdete památky, poznáte Vídeň a v klidu si dáte originál Sacher dort a vídeňskou kávu.</p>", "center"),
])], width=820, extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "16", "left": "24", "isLinked": False}}))
for i in range(0, len(gal), 3):
    P.append(section([column([image(p, c)], 33.333, mobile=50) for p, c in gal[i:i + 3]], pad=8, pad_m=0))
P.append(section([column([])], pad=40, pad_m=24))

# 12) Závěrečná výzva + objednávka (formulář SimpleShop beze změny)
P.append(section([column([
    eyebrow("Nový produkt od února 2026", "center"),
    heading(hl("Získejte jasnou trasu, ", "jistotu a klid", " při objevování Vídně"), align="center"),
    text("<p>První měsíc využilo zaváděcí cenu už několik mých sledovatelů. Cena je stále velmi příjemná v porovnání s osobním doprovodem, "
         "a přitom i v on-line verzi dostáváte kompletní informace, které poskytuji při osobním doprovodu městem.</p>"
         "<p>Pokud plánujete návštěvu Vídně, můžete si trasu stáhnout dnes a využít ji kdykoliv později. "
         "Přístup obdržíte okamžitě po zaplacení.</p>", "center"),
])], bg="sbz_krem", width=820, extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "24", "left": "24", "isLinked": False}}))
P.append(section([column([
    heading("Objednat průvodce do kapsy", "h3", align="center"),
    *original_html_widgets(),
], css="sbz-karta")], bg="sbz_krem", width=760, anchor="objednat",
    extra={"padding": {"unit": "px", "top": "8", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

out = ROOT / os.environ.get("SBZ_OUT", "build/den-ve-vidni.json")
out.write_text(json.dumps(P, ensure_ascii=False, indent=1))
print(f"sections: {len(P)} -> {out}")
