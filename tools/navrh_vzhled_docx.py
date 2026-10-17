#!/usr/bin/env python3
"""Návrh jednotného vzhledu všech stránek (vzor: Den ve Vídni a Vídeň – cestovní podpora) jako Wordový dokument ke schválení.

U každé stránky: úvodní sekce (z textů, které na stránce už jsou) a pořadí dalších sekcí. Na konci gramatické opravy
z tools/texty/gramatika.json (ke každé políčko Souhlasím).
Použití: python3 tools/navrh_vzhled_docx.py [navrhy/NAVRH-VZHLED-STRANEK.docx]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from seo_docx import Cm, Document, Pt, RGBColor, WD_ORIENT, nadpis, odstavec, podbarvi, qn, tabulka  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "navrhy/NAVRH-VZHLED-STRANEK.docx"
GRAM = os.path.join(os.path.dirname(__file__), "texty", "gramatika.json")
SB = "https://sandbox.xafour.eu"

# (typ, adresa, název, úvod: (nadtitulek, nadpis, popis, tlačítka, fotka), další sekce)
U = "už hotovo"
STRANKY = [
    # --- A. Rozcestníky ---
    ("A", "/", "Domů",
     ("Váš bod jistoty při objevování Vídně", "Poznejte Vídeň a Rakousko. Objevte moudrost přírody.",
      "Vaše cestovní podpora ve Vídni a okolí. Autorka projektu Přírodou k sobě.",
      "Chci do Rakouska · Chci do přírody", "Home-1.jpg"),
     "Dvě velké karty vedle sebe (Do Rakouska / Do přírody) s fotkou, krátkým textem a tlačítkem → pás s citátem „Život je výzva "
     "a cesta je cíl“ → „Tak kam povedou vaše kroky“: 3 karty služeb (cestovní podpora, skupiny, průvodce do kapsy) → 3 karty "
     "přírody (Přírodou k sobě, Přírodou ke zdraví, Příroda u vás doma) → světlý pás „Mou láskou je příroda…“ → „Co u mne ještě "
     "najdete“: 4 karty → 3 karty o mně a projektu. Pozn.: věta „On-line průvodkyně Rakouskem“ z úvodu vypadne (slovo průvodkyně)."),
    ("A", "/do-rakouska/", "Do Rakouska",
     ("Do Rakouska", "Začněte teď hned objevovat zajímavosti Vídně a Rakouska.",
      "Jsem Češka žijící ve Vídni, která vám s tím ráda pomůže.", "Cestovní podpora · Tipy na výlety", "do-Rakouska.jpg"),
     "Krátký úvodní text → nadpis VÍDEŇ + 3 karty (dnešní otočné kartičky nahradí karty s fotkou, textem a tlačítkem – na mobilu se "
     "otočné kartičky špatně ovládají) → 3 karty produktů → nadpis RAKOUSKO + 3 karty → světlý pás s odkazem na blog."),
    ("A", "/do-prirody/", "Do přírody",
     ("Do přírody", "Vydejte se do přírody, přírodou k sobě, ke zdraví a harmonii.",
      "Regenerační vycházky do přírody, esence z přírody, aromaterapie a další.", "Zjistit více", "do-prirody-1.jpg"),
     "Text „Objevte se mnou moudrost přírody…“ → 3 karty (místo otočných kartiček) → světlý pás „V přírodě zakoušíme okamžité "
     "uvolnění…“ → závěrečná výzva s tlačítkem."),
    ("A", "/produkty-ke-stazeni/", "Produkty ke stažení",
     ("e-Průvodci, miniprůvodci, příručky a další", "Produkty ke stažení",
      "Abyste si své dny opravdu užili.", "Prohlédnout produkty", "Ke-stazeni-new2.jpg"),
     "Krátké představení (Jsem Češka, žijící…) → mřížka karet produktů (obálka, název, 1–2 věty, tlačítko), placené a zdarma "
     "v jednom jednotném stylu → reference v kartách."),
    ("A", "/pruvodce-a-minipruvodce/", "e-Průvodci a miniprůvodci",
     ("Série e-průvodců a miniprůvodců", "e-Průvodci a miniprůvodci Rakouskem",
      "Osobní zkušenosti, informace a rady, které v průvodcích nenajdete, od Češky žijící v Rakousku.", "Prohlédnout průvodce",
      "e-Pruvodci-zahlavi.jpg"),
     "Mřížka karet průvodců (obálka, název, popis, tlačítko) → pás s výhodami."),
    ("A", "/workshopy-akce/", "Workshopy a akce",
     ("Workshopy a pobyty", "Workshopy a akce", "Workshopy a pobyty pro relaxaci, poznávání přírody i sebe.",
      "Workshopy · Pobyty", "Workshopy-a-akce.jpg"),
     "Věta „Většina akcí je setkání naživo…“ → 2 velké karty (Workshopy / Relaxační a regenerační pobyty)."),
    ("A", "/vylety/", "Výlety",
     ("Tipy na výlety", "Skvělé tipy na výlety v Rakousku.",
      "Vydejte se na výlety do přírody ve Vídni, v okolí Vídně i v celém Rakousku.", "Prohlédnout výlety", "VYLETY.jpg"),
     "Světlý pás s textem „Co nás vlastně pohání…“ → výpis výletů v kartách → odkaz na facebookovou skupinu."),
    ("A", "/vylety-v-rakousku/", "Výlety v Rakousku",
     ("Ve Vídni, v okolí Vídně a v celém Rakousku", "Tipy na výlety", "Vychutnejte rakouskou přírodu všemi smysly.",
      "Prohlédnout výlety", "VYLETY.jpg"),
     "3 výhody jako karty s ikonou → výpis výletů v kartách → reference v kartách."),
    ("A", "/blog/", "Blog",
     ("Blog", "Vydejte se s Blankou za hranice vlasti a denní rutiny.",
      "Články jsou inspirované životem v Rakousku a pobytem v přírodě.", "–", "Blog-uprav.jpg"),
     "Menu kategorií jako řada tlačítek → výpis článků v kartách (stejné karty jako jinde na webu)."),

    # --- B. Služby a pobyty (vzor Vídeň – cestovní podpora) ---
    ("B", "/viden-cestovni-podpora/", "Vídeň – individuální cestovní podpora", (U, U, U, U, U),
     "Nový vzhled je hotový a schválený (stránka …-novy-design). Po vyplnění dokumentu s texty jen přenesu na původní adresu."),
    ("B", "/viden-s-podporou-za-zady/", "Vídeň s podporou za zády",
     ("Cestovní podpora", "Zažijte Vídeň jinak", "Nechte to na mě a využijte službu cestovní podpory – abyste si své dny ve Vídni "
      "opravdu užili!", "Mám zájem · Jak to funguje", "do-hlavicky1.jpg"),
     "Stejné pořadí jako Vídeň – cestovní podpora: pro koho to je (karta) → co získáte (seznam s fajfkami) → varianty služby "
     "v kartách → reference → formulář."),
    ("B", "/viden-s-programem-cestovni-podpora/", "Vídeň a okolí s programem",
     ("Pro skupiny a firmy", "Cestovní podpora Vídeň a okolí s programem pro skupiny a firmy.",
      "…poznejte metropoli Rakouska jako místní s Češkou žijící ve Vídni.", "Poptat program · Reference",
      "skupinova-podpora.jpg"),
     "Otázky „Už nějaký ten čas plánujete…“ ve světlém pásu → pro koho je služba vhodná (seznam) → co je v ceně (karty) → "
     "ukázky programů (karty s fotkou) → reference → formulář."),
    ("B", "/viden-relaxacni/", "Vídeň relaxační",
     ("Necestuj sám(a)", "Poznávací a relaxační pobyt ve Vídni v malé skupince stejně naladěných lidí.",
      "3 dny ve Vídni s prohlídkou historického centra města a návštěvou lázeňského města Baden.", "Chci jet · Program",
      "Upoutavka-na-soc.site_.png"),
     "Co / Kde / Jak jako 3 karty s ikonou → program po dnech (den 1, 2, 3 pod sebou s fotkou) → co je v ceně → cena a "
     "termín v kartě → reference → přihláška."),
    ("B", "/viden-adventni/", "Vídeň adventní",
     ("Necestuj sám(a)", "Třídenní poznávací pobyt ve Vídni v malé skupince stejně naladěných lidí.",
      "3 dny ve Vídni s prohlídkou historického centra města a tradičních vánočních trhů.", "Chci jet · Program",
      "VOUCHER-small.jpg"),
     "Stejně jako Vídeň relaxační."),
    ("B", "/pobyty-nabidka/", "Pobyty a akce v zahraničí",
     ("Místa s krásnou přírodou pro relaxaci a poznávání", "Pobyty v Rakousku i v zahraničí.",
      "Nabízím vám spolucestování v malé skupince žen.", "Aktuální pobyty · Reference", "Akce-a-pobyty2.jpg"),
     "Úvodní text → aktuální pobyty jako karty (fotka, termín, místo, tlačítko) → minulé pobyty a reference."),
    ("B", "/workshopy/", "Workshopy",
     ("Živá setkání", "Workshopy. Živá setkání.", "Off-line živá setkání v malých skupinkách.", "Termíny 2026",
      "Workshopy-1.jpg"),
     "Termíny 2026 jako karty po měsících (měsíc, datum, místo, cena, popis, tlačítko) → reference → formulář."),
    ("B", "/prirodou-k-sobe/", "Přírodou k sobě",
     ("Sebepéče a seberozvoj v přírodě", "Přírodou k sobě",
      "Regenerační procházky do přírody s použitím prvků Lesní mysli, Lesní terapie, Tai-Chi a Qi-Gong.",
      "Termíny procházek", "Prirodou-k-sobe.jpg"),
     "Text „Well-being v přírodě…“ s fotkou → co vám procházky dají (seznam) → termíny a místa (karta) → reference."),
    ("B", "/regeneracni-prochazky/", "Regenerační procházky",
     ("Přírodou k sobě", "Regenerační procházky do přírody",
      "S využitím prvků Lesní mysli, Lesní terapie, Tai-Chi a Čchi-Kung.", "Chci informace o termínech",
      "Prochazky-do-prirody.jpg"),
     "Autorský projekt (text s fotkou) → termíny a místa: Vídeň a Praha jako 2 karty se srazem a dopravou → "
     "„Kdo vás bude přírodou provázet“ → reference."),
    ("B", "/prirodou-ke-zdravi-s-blankou-k-bewit/", "Přírodou ke zdraví (fialková)",
     ("Esence přírody", "Přírodou ke zdraví a harmonii.", "Využijte esence přírody pro podporu těla, mysli i duše.",
      "O svůj voňavý dárek se přihlaste zde", "Prirodou-ke-zdravi.jpg (levandule)"),
     "Jen tato stránka má místo broskvové barvy levandulovou (viz barvy níže). Pořadí: osobní směs na míru (text s fotkou) → "
     "„Cesta k esenciálním olejům…“ seznam „I vy můžete…“ → otázky a odpovědi v kartě vedle obrázku → dárkový balíček → "
     "formulář."),
    ("B", "/nabidka-pro-kolektivy/", "Nabídka pro kolektivy",
     ("Školy a dětské skupiny", "Nabídka pro kolektivy, školy a dětské skupiny.",
      "Hluboké propojení s přírodou, hluboké propojení se sebou.", "Vybrat téma · Video ukázka", "Nabidka-komplet.jpg"),
     "Úvodní text → témata jako mřížka karet 2 × 3 (Příroda na talíři, Přírodou k sobě, Aromaterapie, Rokem krok za krokem, "
     "Příroda jako tělocvična, Kontakt) → formulář."),
    ("B", "/spoluprace/", "Spolupráce",
     ("Pojďme spolupracovat", "Vzájemně přínosná podpora a spolupráce dává smysl.",
      "Síly i výhody se násobí a přináší efekt oběma stranám.", "Napsat mi", "Spoluprace1.jpg"),
     "2 velké karty vedle sebe (Žena-podnikatelka / Firma, zařízení, instituce) s fotkou a textem → formulář."),
    ("B", "/bonusy-pro-klienty/", "Bonusy pro klienty",
     ("Bonusy, výhody, slevy", "Bonus navíc pro klienty cestovní podpory",
      "Všichni, kdo si u mne objednají jakoukoliv formu cestovní podpory, mají možnost si vybrat bonus navíc.",
      "Vybrat bonus", "FOTO-NA-www.-STRANKU-VYHOD.jpg"),
     "Mřížka 12 bonusů v kartách (3 vedle sebe) → podmínka „Výběr bonusu je nutné uvést…“ ve světlém pásu → formulář."),

    # --- C. Produkty (vzor Den ve Vídni) ---
    ("C", "/den-ve-vidni/", "Den ve Vídni", (U, U, U, U, U),
     "Nový vzhled je hotový a schválený (stránka …-novy-design). Po vyplnění dokumentu s texty jen přenesu na původní adresu."),
    ("C", "/minipruvodce-vidni-snadno/", "Miniprůvodce Vídní",
     ("Miniprůvodce", "Poznejte Vídeň jako místní – bez stresu, shonu a bez zbytečných výdajů.",
      "Přestaňte bloudit a začněte si metropoli užívat.", "Objednat miniprůvodce · Co obsahuje", "Viden.jpg"),
     "Stejné pořadí jako Den ve Vídni: co to je (text + obálka) → „Znáte to…“ seznam → 5 přínosů jako karty s ikonou → "
     "fotky → benefity → „Není, co ztratit“ → reference → pro koho je / není (2 karty) → kdo ho vytvořil → objednávka. "
     "Stránka dostane i hlavičku a patičku webu (dnes je bez nich)."),
    ("C", "/pruvodce-viden-zahrady-a-parky/", "e-Průvodce Vídeň: parky a zahrady",
     ("e-Průvodce Vídeň", "5 nejkrásnějších parků a zahrad",
      "Unikněte turistickému shonu a objevte klidná zákoutí Vídně.", "Koupit průvodce · Co obsahuje",
      "Hlavni-obrazek-small.jpg"),
     "Stejné pořadí jako Den ve Vídni. Stránka dostane i hlavičku a patičku webu (dnes je bez nich)."),
    ("C", "/7-nejcastejsich-chyb-turistu-ve-vidni/", "7 nejčastějších chyb turistů",
     ("Praktická příručka zdarma", "7 nejčastějších chyb turistů ve Vídni… a jak se jim vyhnout.",
      "I drobné chyby mohou znepříjemnit váš pobyt ve Vídni.", "Získat příručku", "Hlavicka-4b.jpg"),
     "Úvod s obálkou → co v příručce najdete (seznam) → reference v kartách → „Stažením dárku nic neriskujete“ → tlačítko. "
     "Pozn.: „Praktické tipy od místní průvodkyně“ je potřeba přeformulovat (viz otázky)."),
    ("C", "/checklist-na-vylety/", "Checklist na výlety",
     ("Dárek zdarma", "Checklist – 10 věcí, na které je dobré myslet, než se vydáte na výlet",
      "Co zabalit do batohu pro pohodu na cestách a výletech.", "To potřebuji", "obalka-checklist.jpg"),
     "Stejně jako 7 chyb turistů."),
    ("C", "/tahak-na-vyuku-nemciny/", "Tahák na výuku němčiny",
     ("Dárek zdarma", "Tahák na výuku němčiny – 3 skvělé tipy, jak se naučit jazyk hravě a vtipně",
      "Včetně tří praktických video ukázek.", "To se hodí", "vystrizek-novy2.jpg"),
     "Stejně jako 7 chyb turistů."),
    ("C", "/vidni-pesky-i-na-kole/", "Vídní pěšky i na kole",
     ("Praktická příručka zdarma", "Vídní pěšky i na kole",
      "3 + 3 tipy, jak si usnadnit poznávání Vídně pro pěší i cykloturisty.", "Získat příručku", "OBALKA-a-nahled.jpg"),
     "Stejně jako 7 chyb turistů."),
    ("C", "/dekorace-rokem-krok-za-krokem/", "Dekorace – Rokem krok za krokem",
     ("Dekorace do bytu", "Rokem krok za krokem.", "Vytvořte si jednoduché dekorace do bytu.", "Chci tvořit",
      "Dekorace-1.jpg"),
     "Co vás čeká (seznam) → video ukázka → formulář → 12 měsíců jako mřížka karet 3 × 4 (fotka, měsíc, popis) → reference."),

    # --- D. Poděkování (stejná krátká šablona) ---
    ("D", "/checklist-na-vylety-podekovani/", "Checklist – poděkování",
     ("Děkuji", "Děkuji vám za váš zájem o checklist na výlety", "Váš e-mail dorazil v pořádku do mé schránky.", "–",
      "obrázek checklistu"),
     "3 kroky jako očíslované karty (1 potvrzovací e-mail, 2 e-mail s dárkem, 3 když nic nepřišlo → složka SPAM) → přání."),
    ("D", "/tahak-na-vyuku-nemciny-podekovani/", "Tahák – poděkování", ("Děkuji", "Děkuji vám za váš zájem o tahák na výuku němčiny",
     "Váš e-mail dorazil v pořádku do mé schránky.", "–", "3D-s-mobilem.jpg"), "Stejně jako Checklist – poděkování."),
    ("D", "/vidni-pesky-i-na-kole-podekovani/", "Vídní pěšky – poděkování", ("Děkuji", "Děkuji vám za váš zájem o praktickou "
     "příručku Vídní pěšky i na kole", "Váš e-mail dorazil v pořádku do mé schránky.", "–", "Vidni-pesky-i-na-kole-1-ZAHLAVI.jpg"),
     "Stejně jako Checklist – poděkování."),
    ("D", "/odber-novinek/", "Odběr novinek", ("Vítejte zpět", "Tak tě vítám zpět. Je fajn, že o žádné novinky nepřijdeš.",
     "Byla by škoda nevyužít všech informací.", "Na úvodní stránku", "str.404-2.jpg"),
     "2 karty (Do Rakouska / Do přírody) → dárek pexeso."),

    # --- E. O mně a projektu ---
    ("E", "/o-mne/", "Kdo je Blanka",
     ("Z Prahy do Vídně", "Co dělá Češka v Rakousku?",
      "Jmenuji se Blanka, a právě teď žiji za hranicí své vlasti i své denní rutiny.", "Můj příběh · Kontakt", "O-MNE.jpg"),
     "Text a fotka střídavě vlevo a vpravo → bloky „Jsem…“ ve světlém pásu → karta s nabídkou (němčina) → výlety → tlačítko."),
    ("E", "/muj-pribeh/", "Můj příběh",
     ("Můj příběh", "Jmenuji se Blanka, a právě teď žiji za hranicí své vlasti i své denní rutiny.",
      "Jsem žena (narozena ve znamení Kozoroha)…", "–", "zahlavi-muj-pribeh2.jpg"),
     "Dlouhý text v úzkém sloupci, aby se dobře četl → mezinadpisy (Kristova léta, o 10 let později…) jako kapitoly → fotky "
     "mezi kapitolami → důležité věty jako citát ve světlém pásu."),
    ("E", "/jak-se-zije-za-hranici/", "Jak se žije za hranicí",
     ("Život v zahraničí", "Příběhy žen, které se vydaly na zkušenou do světa.",
      "Navštivte 6 různých zemí prostřednictvím autentických příběhů obyčejných a přitom neobyčejně zajímavých žen.",
      "Přečíst příběhy", "Jak-se-zije-za-hranici.jpg"),
     "6 příběhů jako karty (země, jméno, úryvek, odkaz) → Anička (text s fotkou) → fotky."),
    ("E", "/projekt-v-mediich/", "Projekt v médiích",
     ("Rozhovory, reportáže, články", "Spolupráce s médii. Rádio, televize, noviny.", "–", "–", "Media-small.jpg"),
     "Každé médium jako karta (datum a médium, fotka, text, odkaz na záznam) – nejnovější nahoře."),
    ("E", "/reference/", "Reference",
     ("Co říkají klienti", "Reference zákazníků", "Co o mých službách a produktech říkají klienti.", "–", "Home-1.jpg"),
     "6 karet (individuální podpora, skupiny, výlety, pobyty, workshopy, produkty), každá s tlačítkem na reference."),
    ("E", "/kontakt-s-blankou-za-hranice/", "Kontakt",
     ("Kontakt", "Kde mne najdete a jak mne můžete kontaktovat.",
      "Najdete mě střídavě ve Vídni a v Praze – ve dvou krásných metropolích.", "–", "KONTAKT.jpg"),
     "Dva sloupce: vlevo formulář, vpravo adresa, mapka a sociální sítě → karta Spolupráce."),
    ("E", "/fotogalerie/", "Fotogalerie",
     ("Fotogalerie", "Fotogalerie", "Krátká fotoochutnávka z výletů po Rakousku, koučovacích procházek do přírody a z tvorby "
      "přírodních dekorací do bytu.", "–", "zahlavi-HOME.jpg"),
     "Galerie jako jednotná mřížka se zaoblenými rohy, každá s nadpisem a tlačítkem."),
    ("E", "/fotogalerie-bonus/", "Fotogalerie – bonus", ("Fotogalerie", "Fotogalerie – bonus plus",
     "Bonusová fotoochutnávka z výletů po Rakousku, které na webu nenajdete.", "–", "zahlavi-HOME.jpg"),
     "Stejně jako Fotogalerie."),
    ("E", "/dekorace-do-bytu/", "Dekorace", ("Dekorace do bytu", "Rokem krok za krokem.",
     "Vyrobte si jednoduché přírodní dekorace do bytu.", "–", "Dekorace.jpg"),
     "Text → výpis článků v kartách → „Jak se zrodil projekt“ ve světlém pásu."),
]
TYPY = {
    "A": ("Rozcestníky", "Stránky, ze kterých se jde dál. Po úvodu následují karty (fotka, nadpis, 1–2 věty, tlačítko)."),
    "B": ("Služby, pobyty a akce – vzor Vídeň – cestovní podpora", "Úvod → pro koho to je → co získáte → nabídka v kartách → reference → formulář."),
    "C": ("Produkty a dárky ke stažení – vzor Den ve Vídni", "Úvod → co to je (text a obálka) → co obsahuje → přínosy → reference → objednání nebo stažení."),
    "D": ("Poděkování po přihlášení", "Krátká stránka: nižší úvod a 3 očíslované kroky."),
    "E": ("O mně a projektu", "Klidnější stránky s delším textem: úzký sloupec, fotky mezi odstavci, citáty ve světlém pásu."),
}
OTAZKY = [
    "Nadpisy psané celé velkými písmeny (např. CESTOVNÍ PODPORA, PRŮVODCE, CHECKLIST) navrhuji psát běžně, jako na "
    "stránkách Den ve Vídni a Cestovní podpora – zvýraznění pak dělá barva a tučné písmo. Souhlasíte?",
    "Zkušební stránky (varianty úvodu, palety, Test) po schválení vzhledu smažu, aby se nepletly. Souhlasíte?",
    "Stránky Obchodní podmínky, Ochrana osobních údajů a Zásady cookies: navrhuji jen nový úvod (nízký pruh s nadpisem) "
    "a čitelnou šířku textu, obsah beze změny. Souhlasíte?",
]


def barvy(doc):
    """Ukázka dvou palet: hlavní (Louka a broskev) a levandulová jen pro Přírodou ke zdraví."""
    palety = [
        ("Celý web – Louka a broskev (beze změny)", [("Tmavě zelená", "145A38"), ("Světle olivová", "DEE5A3"),
                                                      ("Broskvová (pozadí)", "F5E1CF"), ("Terakota (drobnosti)", "A8653F"),
                                                      ("Krémová", "FBF7F0")]),
        ("Jen Přírodou ke zdraví – Louka a levandule", [("Tmavě zelená", "145A38"), ("Světle olivová", "DEE5A3"),
                                                         ("Levandulová (pozadí)", "E8E0F2"), ("Fialková (drobnosti)", "6E4E8E"),
                                                         ("Krémová", "FAF8FC")]),
    ]
    for nazev, barvy_ in palety:
        odstavec(doc, nazev, None).runs[0].bold = True
        t = doc.add_table(rows=2, cols=len(barvy_))
        t.style = "Table Grid"
        for i, (jm, hexa) in enumerate(barvy_):
            podbarvi(t.rows[0].cells[i], hexa)
            t.rows[0].cells[i].paragraphs[0].add_run(" ").font.size = Pt(18)
            r = t.rows[1].cells[i].paragraphs[0].add_run(f"{jm}\n#{hexa}")
            r.font.size = Pt(8)
        doc.add_paragraph()


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

    nadpis(doc, "Jednotný vzhled všech stránek – návrh ke schválení", 0)
    odstavec(doc, "Připraveno 17. 10. 2026. Zatím je to jen návrh, na webu se nic nezměnilo. Texty zůstávají vaše, "
             "opravím jen gramatické chyby (seznam je na konci). Vzorem jsou stránky, které už máte schválené:")
    for t in (f"{SB}/den-ve-vidni-novy-design/", f"{SB}/viden-cestovni-podpora-novy-design/"):
        odstavec(doc, t).style = "List Bullet"

    nadpis(doc, "Jak dokument vyplnit")
    for t, txt in [
        ("Návrh je v pořádku: ", "klikněte na políčko ☐ ve sloupci Souhlasím (změní se na ☒)."),
        ("Chcete něco jinak: ", "napište to do sloupce Vaše změna (jiný nadpis, jiná fotka, jiné pořadí…)."),
        ("Hotovo: ", "dokument uložte do složky Dokumenty a napište mi. Stránky pak předělám na zkušebním webu "
                     "a pošlu vám odkazy na kontrolu."),
    ]:
        odstavec(doc, txt, t).style = "List Bullet"

    nadpis(doc, "Co bude na všech stránkách stejné")
    for t, txt in [
        ("Úvodní sekce: ", "fotka přes celou šířku se světlým závojem, nahoře malý nadtitulek, pod ním velký nadpis, "
                           "1–2 věty popisu (tmavé tučné písmo se světlou září) a 1–2 tlačítka. Stejně jako na obou vzorech."),
        ("Písmo: ", "nadpisy Lora (s patkami), ostatní text Source Sans 3."),
        ("Barvy: ", "paleta Louka a broskev. Sekce se střídají: bílá → krémová → broskvová → bílá. "
                    "Výjimka: Přírodou ke zdraví má místo broskvové levandulovou (ukázka níže)."),
        ("Tlačítka: ", "hlavní tmavě zelené, vedlejší světle olivové. Stejný tvar na celém webu."),
        ("Karty: ", "bílé rámečky se zaoblenými rohy a jemným stínem. Nahradí dnešní otočné kartičky, obrázkové boxy a různé rámečky."),
        ("Fotky: ", "zaoblené rohy, stejné odsazení. Šipky a dekorativní oddělovače zmizí."),
        ("Mobil: ", "vše pod sebou, tlačítka přes celou šířku, písmo dost velké na čtení."),
    ]:
        odstavec(doc, txt, t).style = "List Bullet"
    barvy(doc)

    nadpis(doc, "Otázky")
    tabulka(doc, ["Otázka"], [17.0], [[q] for q in OTAZKY], souhlas=False)

    for typ, (nazev, popis) in TYPY.items():
        nadpis(doc, f"{typ}. {nazev}")
        odstavec(doc, popis)
        radky = []
        for t, adr, jm, (nt, h1, pop, btn, foto), dalsi in STRANKY:
            if t != typ:
                continue
            if nt == U:
                uvod = "Hotovo – úvod je schválený."
            else:
                uvod = f"Nadtitulek: {nt}\nNadpis: {h1}\nPopis: {pop}\nTlačítka: {btn}\nFotka: {foto}"
            radky.append([(jm, adr), uvod, dalsi])
        tabulka(doc, ["Stránka", "Úvodní sekce", "Další sekce (pořadí)"], [3.4, 6.2, 7.4], radky)

    if os.path.exists(GRAM):
        g = json.load(open(GRAM, encoding="utf-8"))
        nadpis(doc, "Slovo průvodce / průvodkyně o vás")
        odstavec(doc, "Tato místa obsahují slovo průvodce nebo průvodkyně ve významu osoby. Navrhuji tato znění; "
                 "kde píšu „ponechat“, jde o obecné použití, ne o vás.")
        tabulka(doc, ["Stránka", "Teď", "Návrh"], [3.4, 6.8, 6.8],
                [[x["stranka"], x["puvodne"].lstrip("# "), x["navrh"]] for x in g["pruvodce"]])

        nadpis(doc, "Gramatické opravy")
        typo = g["typografie"]
        odstavec(doc, f"Celkem {len(g['opravy'])} oprav. Z toho {sum(typo.values())} jsou drobnosti, které opravím bez ptaní: "
                 "spojovník „-“ místo pomlčky „–“, rovné uvozovky \"…\" místo českých „…“ a chybějící nebo přebytečné mezery. "
                 "Ostatní opravy (čárky, překlepy, shoda, i/y, mě/mně…) jsou v tabulce. Nechcete-li některou, napište "
                 "do sloupce Vaše změna „NE“.")
        radky, minula = [], None
        for x in g["opravy"]:
            if x.get("typografie"):
                continue
            radky.append([x["stranka"] if x["stranka"] != minula else "", x["puvodne"].lstrip("# "),
                          (x["opraveno"].lstrip("# "), x["duvod"])])
            minula = x["stranka"]
        tabulka(doc, ["Stránka", "Teď", "Opraveno"], [3.4, 6.8, 6.8], radky)

    doc.save(OUT)
    print(OUT, len(STRANKY), "stránek")


if __name__ == "__main__":
    main()
