"""Postaví novou verzi stránky „Vídeň – individuální cestovní podpora“ v jednotném designu.

Vstup: snapshots/post-19575.json (původní stránka). Texty, fotky a reference se berou z ní.
Výstup: build/viden-podpora.json. Spuštění: python3 tools/build_viden_podpora.py
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sbz import *  # noqa: E402,F401,F403
import sbz  # noqa: E402

load("post-19575.json", prefix="sbz-viden")
testimonials = sbz.testimonials

UVOD = os.environ.get("SBZ_UVOD", "krem")  # styl úvodní fotky, viz sbz.hero

# ---------- stránka ----------
P = []

# 1) Úvod (hero)
P.append(hero("Individuální cestovní podpora ve Vídni", "Vídeň bez starostí, na míru a s podporou za zády",
              "<p>Nechte si ušít návštěvu Vídně na míru a proměňte běžný výlet v nezapomenutelný zážitek.</p>",
              [("Domluvit 15 minut zdarma", TELEFON), ("Objednat službu", OBJEDNAT_PODPORU)],
              "2026/10/zahlavi-cestovni-podpora-2026.jpg", UVOD, 560))

# 2) Chystáte se do Vídně?
P.append(section([column([
    heading("Chystáte se do Vídně?", "h2", align="center"),
])], bg="sbz_krem", pad=72, pad_m=48, extra={"padding": {"unit": "px", "top": "44", "right": "24", "bottom": "16", "left": "24", "isLinked": False},
                                              "padding_mobile": {"unit": "px", "top": "32", "right": "16", "bottom": "12", "left": "16", "isLinked": False}}))
P.append(section([
    column([icon_box("fas fa-hourglass-half", "Nemáte čas trávit hodiny hledáním, kam se podívat?")], 33.333),
    column([icon_box("fas fa-route", "Nevíte si rady s plánováním cesty?")], 33.333),
    column([icon_box("fas fa-comments", "Bojíte se, že se nedomluvíte?")], 33.333),
], bg="sbz_krem", pad=16))
P.append(section([column([
    heading("Nechte to na mě a využijte službu cestovní podpory, abyste si své dny ve Vídni opravdu užili.",
            "h3", align="center", color="sbz_zelena"),
])], bg="sbz_krem", pad=24, extra={"padding": {"unit": "px", "top": "24", "right": "24", "bottom": "80", "left": "24", "isLinked": False}}, width=820))

# 3) Na míru + Zažijte Vídeň jinak
P.append(section([
    column([
        eyebrow("Služba na míru"),
        heading("Nechte si ušít návštěvu Vídně na míru"),
        text("<p>Vídeň nabízí tolik krásných míst a zážitků, že bez místního průvodce snadno minete to nejlepší. "
             "Jako Češka, žijící ve Vídni už 10 let, vám pomohu objevit skutečnou duši tohoto města a vyhnout se turistickým pastem.</p>"
             "<p>Mé služby jsou navržené tak, abyste z Vídně získali maximum, ať už máte na návštěvu den nebo týden.</p>"),
        heading("Zažijte Vídeň jinak", "h3"),
        icon_list(["Bez starostí a v klidu.", "Bez bloudění a ztráty času.", "S informacemi, které se hodí."]),
    ], 55, valign="middle"),
    column([image("2023/09/do-hlavicky1.jpg", css="sbz-foto-vysoka sbz-bez-ramu")], 45, valign="middle"),
], valign="middle"))

# 4) Tři pilíře služby
P.append(section([
    column([icon_box("fas fa-map-marked-alt", "Itineráře na míru", "Plán cesty přesně podle vašich přání, tempa a délky pobytu.")], 33.333),
    column([icon_box("fas fa-hands-helping", "Organizační pomoc na místě", "Jízdenky, doprava, orientace ve městě – vyřešíme to spolu.")], 33.333),
    column([icon_box("fas fa-walking", "Osobní doprovod ve Vídni", "Procházka městem s příběhy, které v průvodcích nenajdete.")], 33.333),
], pad=0, pad_m=0, extra={"padding": {"unit": "px", "top": "0", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 5) Tahle nabídka je i pro vás
P.append(section([
    column([image("2023/09/do-hlavicky2.jpg", css="sbz-foto-vysoka sbz-bez-ramu")], 40, valign="middle"),
    column([
        heading(hl("Tahle nabídka je ", "i pro vás")),
        icon_list([
            "Pokud jedete do Vídně a <strong>nechcete bloudit a ztrácet čas</strong>.",
            "Pokud chcete <strong>ušetřit dlouhé minuty a hodiny hledání</strong> na internetu.",
            "Pokud budete Vídní projíždět a <strong>chcete svůj čas efektivně využít</strong>.",
            "Pokud <strong>máte jasnou představu a nevíte, kde přesně hledat</strong>.",
            "Pokud by se vám hodil <strong>předem rámcový plán cesty</strong>.",
            "Pokud chcete <strong>zažít město očima obyvatelky Vídně</strong> se skutečným životem, a ne jen prostřednictvím „suchých dat a letopočtů“.",
            "Pokud <strong>jste si nejistí kvůli němčině</strong> a bojíte se, že se v Rakousku nedorozumíte.",
        ]),
    ], 60, valign="middle"),
], bg="sbz_krem", valign="middle"))

# 6) Výzva k akci
P.append(section([column([
    heading("Nechte si připravit detailní plán cesty na míru nebo využijte podporu na místě", "h2",
            align="center"),
    text("<p>Dejme si 15minutovku zdarma a řekněte mi své představy.</p>", "center"),
    button("Zavolat hned pro domluvu", TELEFON, "primary", inline=True),
    button("Pošlete mi telefon, ozvu se vám", KONTAKT, "secondary", inline=True),
    text("<p>Nebuďte zaskočeni, volat vám bude rakouské číslo.</p>", "center", "sbz_seda", "sbz_maly"),
], align="center")], bg="sbz_louka", pad=80, width=860))

# 7) Průvodce do kapsy
P.append(section([
    column([image("2026/03/houpaci-kreslo.png", css="sbz-foto", link="/den-ve-vidni/")], 40, valign="middle"),
    column([
        eyebrow("Ekonomičtější varianta"),
        heading("Neshodneme se v termínu nebo chcete ušetřit?"),
        text("<p>Pak se vám bude hodit on-line <strong>Průvodce do kapsy</strong> – stejná trasa, kterou chodím s klienty při osobním doprovodu.</p>"
             "<p>Trasa širším centrem Vídně s popisem památek a mapkou ke stažení do mobilu. Vede vás jasně, klidně a bez zbytečného zdržování. "
             "Nebloudíte, nehledáte a máte jistotu, že jdete správně. Roky prověřená trasa a spokojení klienti.</p>"
             "<p><strong>Váš bod jistoty při objevování Vídně – klidný den za 40 € / 980 Kč.</strong></p>"),
        button("Vyzkouším Průvodce do kapsy", OBJEDNAT_PRUVODCE, "primary", inline=True),
        button("Více o průvodci", "/den-ve-vidni/", "secondary", inline=True),
    ], 60, valign="middle"),
], valign="middle"))

# 8) Proč využít
P.append(section([column([
    heading(hl("Proč využít ", "cestovní podporu", " nebo Průvodce do kapsy"), align="center"),
])], bg="sbz_krem", extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "24", "left": "24", "isLinked": False}}))
P.append(section([
    column([icon_list([
        "<strong>Ušetříte čas</strong> hledáním v průvodcích, co ve Vídni navštívit a kudy se k památkám dostat.",
        "<strong>Neztratíte se ve výběru</strong> a pořizování nejvýhodnějších jízdenek městské dopravy.",
        "<strong>Snadno se zorientujete v dopravě</strong> a zjistíte, jak nejlépe z místa A do místa B.",
        "<strong>Během jednoho odpoledne projdete</strong> kolem nejznámějších turistických cílů Vídně.",
    ])], 50),
    column([icon_list([
        "<strong>Lehce najdete legendární Hotel Sacher</strong>, kde si v kavárně vychutnáte pravou vídeňskou kávu a Sacher dort.",
        "<strong>Dozvíte se něco praktického z běžného života ve Vídni</strong> a poznáte Rakousko autentičtěji.",
        "<strong>Užijete si své dny naplno</strong>, protože budete mít ve Vídni pomoc a podporu za zády.",
    ])], 50),
], bg="sbz_krem", pad=8))
P.append(section([
    column([image("2023/05/Hofburg.jpg", "Hofburg")], 33.333, mobile=50),
    column([image("2023/05/Karlskirche.jpg", "Karlskirche")], 33.333, mobile=50),
    column([image("2023/05/Opera.jpg", "Státní opera")], 33.333, mobile=50),
], bg="sbz_krem", pad=24))
P.append(section([column([
    button("Tak to se hodí, chci cestovní podporu", OBJEDNAT_PODPORU, "primary", inline=True),
    button("Vyzkouším Průvodce do kapsy", OBJEDNAT_PRUVODCE, "secondary", inline=True),
], align="center")], bg="sbz_krem", extra={"padding": {"unit": "px", "top": "16", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 9) Jak spolupráce probíhá
P.append(section([
    column([
        eyebrow("Individuální cestovní podpora"),
        heading(hl("Jak ", "spolupráce probíhá", "?")),
        text("<ol>"
             "<li>Při prvním kontaktu e-mailem či telefonem si ujasníme vaše přání, představy a potřeby.</li>"
             "<li>Ujasníme si délku a termín vašeho pobytu.</li>"
             "<li>Na základě těchto informací zpracuji nabídku do konkrétní objednávky včetně cenové kalkulace a zašlu vám ji k odsouhlasení.</li>"
             "<li>Po vašem potvrzení začnu na objednávce nebo itineráři pracovat detailně.</li>"
             "<li>Podle potvrzeného harmonogramu vám zašlu finální verzi itineráře či služby.</li>"
             "<li>Potvrdíme si předání dokumentu, případně doupřesníme detaily.</li>"
             "<li>Většinou klientům předem zašlu nebo při příjezdu předám malý dárek navíc – vždy něco, co pomůže při výletu do Vídně.</li>"
             "<li>Pak už se na vás těší Vídeň i já.</li>"
             "</ol>", css="sbz-text sbz-kroky"),
    ], 58),
    column([
        heading("Platba", "h3"),
        text("<p>Platba probíhá ve dvou částech:</p><p><strong>a)</strong> záloha 50 % po potvrzení prvotní objednávky,<br>"
             "<strong>b)</strong> doplatek 50 % po zaslání finální verze itineráře nebo několik dní před vaším příjezdem do Vídně. "
             "Termín splatnosti je vždy součástí objednávky.</p>"),
        heading("Co služba nezahrnuje", "h3"),
        text("<p><strong>Součástí služby není provádění jakýchkoliv rezervací.</strong> Rezervace ubytování, dopravy a podobně si provádíte sami "
             "na základě doporučených podkladů nebo podle vlastního výběru.</p>"),
    ], 42, css="sbz-karta"),
]))

# 10) Co služba zahrnuje
P.append(section([column([
    heading(hl("Co služba cestovní podpory ", "zahrnuje")),
])], bg="sbz_krem", extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "16", "left": "24", "isLinked": False}}))
P.append(section([
    column([icon_list([
        "Doporučení ohledně dopravního spojení.",
        "Doporučení a výběr nejvýhodnějších jízdenek pro městskou dopravu a váš pobyt ve Vídni.",
        "Itinerář na příslušný počet dní včetně trasy prohlídky městem, případně i s mapkou ke stažení do mobilu.",
        "Základní informace o místech a památkách na vaší trase.",
    ])], 50),
    column([icon_list([
        "Doporučení výhodného ubytování – cenou nebo polohou – podle vašich přání.",
        "Na přání osobní vyzvednutí na nádraží a pomoc s prvotní orientací ve městě.",
        "Na přání osobní doprovod po městě nebo na vybrané památky ve Vídni a okolí – půldenní, celodenní i vícedenní program.",
        "Podpora nemusí být po celou dobu pobytu. Často stačí 1–2 dny pro základní nebo hlubší orientaci.",
    ])], 50),
], bg="sbz_krem", extra={"padding": {"unit": "px", "top": "16", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 11) Reference
real = [t for t in testimonials if not t["content"].strip().startswith("Zde může být")]
left, right = real[0::2], real[1::2]
P.append(section([column([
    heading(hl("Přečtěte si ", "reference", " od mých klientů"), align="center"),
])], anchor="individualnipodporareference", extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "24", "left": "24", "isLinked": False}}))
P.append(section([
    column([testimonial(t) for t in left], 50),
    column([testimonial(t) for t in right], 50),
], pad=8))
P.append(section([column([
    text("<p>Zde může být i vaše recenze. Chystáte se do Vídně a chcete pobyt prožít bez stresu a starostí? "
         "Napište mi – program na míru mám i pro vás.</p>", "center"),
    button("Napsat Blance", KONTAKT, "secondary", "center"),
])], width=760, extra={"padding": {"unit": "px", "top": "16", "right": "24", "bottom": "88", "left": "24", "isLinked": False}}))

# 12) Kdo vám bude oporou
P.append(section([
    column([image("2023/11/20170704_183039.jpg", css="sbz-foto-vysoka")], 40, valign="middle"),
    column([
        heading(hl("Kdo vám bude ", "oporou", " ve Vídni")),
        text("<p>Jmenuji se Blanka, jsem Češka a od ledna 2017 žiji ve Vídni. Z Prahy do Vídně jsem se přestěhovala ve věku 50 let. "
             "Byl to velký skok do neznáma, a tak mám stále v živé paměti, jak se člověk v novém prostředí nesnadno orientuje.</p>"
             "<p>Rakousko jsem začala objevovat především prostřednictvím výletů do přírody a postupně se seznamovala se životem ve Vídni. "
             "V roce 2020 vznikl můj projekt „s Blankou za hranice“, ve kterém pomáhám krajanům s poznáváním Vídně a Rakouska. "
             "Jsem milovnice přírody a všeho opravdového.</p>"
             '<p>Více o mně si můžete přečíst <a href="/o-mne/">na stránce Kdo je Blanka</a>, '
             'rozhovor v rádiu ORF si můžete <a href="https://volksgruppen.orf.at/cesi/radiotelevize/stories/3145808" target="_blank" rel="noopener">poslechnout zde</a>.</p>'
             "<p>Těším se na vás v metropoli Rakouska a pomohu vám, abyste si svůj pobyt ve Vídni opravdu užili.</p>"),
        button("Objednat službu", OBJEDNAT_PODPORU, "primary", inline=True),
        button("Poslat zprávu", KONTAKT, "secondary", inline=True),
    ], 60, valign="middle"),
], bg="sbz_krem", valign="middle"))

# 13) Co můžete ve Vídni vidět
gal = [("2023/05/Burggarten-1.jpg", "Schmetterlinghaus"), ("2023/06/Fiakr2-S.jpg", "Typický vídeňský fiakr"),
       ("2023/06/Albertina.jpg", "Albertina"), ("2023/05/Hundertwasserhaus.jpg", "Hundertwasserhaus"),
       ("2023/05/Liliputbahn.jpg", "Vláček v parku Prátr"), ("2023/06/nocni.jpg", "Vídeňská opera"),
       ("2023/05/Belveder-1.jpg", "Zámek Belvedere"), ("2023/05/Belveder-2.jpg", "Zámek Belvedere"),
       ("2023/05/Belveder-3.jpg", "Zámek Belvedere"), ("2023/05/Schonbrunn-1.jpg", "Zámek Schönbrunn"),
       ("2023/05/Schonbrunn-3.jpg", "Zámek Schönbrunn"), ("2023/05/Schonbrunn-2.jpg", "Zámek Schönbrunn"),
       ("2023/05/Hotel-Sacher-Wien.jpg", "Hotel Sacher"), ("2023/05/Sachr-2.jpg", "Originál Sacher dort"),
       ("2023/05/Hofburg-2.jpg", "Hofburg")]
P.append(section([column([
    heading(hl("Co ", "můžete ve Vídni vidět", " a navštívit"), align="center"),
    text("<p>Obejdete památky, poznáte Vídeň a v klidu si dáte originál Sacher dort a vídeňskou kávu.</p>", "center"),
])], width=820, extra={"padding": {"unit": "px", "top": "88", "right": "24", "bottom": "16", "left": "24", "isLinked": False}}))
for i in range(0, len(gal), 3):
    P.append(section([column([image(p, c)], 33.333, mobile=50) for p, c in gal[i:i + 3]], pad=8, pad_m=0))
P.append(section([column([])], pad=40, pad_m=24))

# 14) Bonus
P.append(section([
    column([image("2024/03/Bonusy-slevy-vyhody-obrazek-na-soc.site_-1.png", css="sbz-obrazek")], 40, valign="middle"),
    column([
        eyebrow("A to není zdaleka vše"),
        heading(hl("Bonus = ", "dárek", " pro každého klienta")),
        text("<p>Pro každého klienta, který si objedná jakoukoliv formu služby cestovní podpory, je připraven bonus navíc, "
             "který vám ušetří další náklady. Se službou cestovní podpory ušetříte nejen peníze, ale i čas a nervy.</p>"
             "<p>Bonus má podobu slevy na jednu akci během pobytu. Vybrat si můžete z deseti zajímavých atrakcí pro děti i dospělé, "
             "návštěv typických restaurací nebo vstupů na zajímavá turistická místa v metropoli Rakouska.</p>"),
        button("Seznam bonusů", "/bonusy-pro-klienty/", "secondary"),
    ], 60, valign="middle"),
], bg="sbz_krem", valign="middle"))

# 15) Pro skupiny
P.append(section([
    column([
        eyebrow("Pro firmy, školy a spolky"),
        heading(hl("Nabídku připravím ", "i pro skupiny")),
        text("<p>Na základě služby cestovní podpory mohu stejně nebo podobně připravit výlety a pobyty ve Vídni a okolí i pro vaši organizaci. "
             "Některé věci budete mít zajištěné a nemusíte se o ně starat, něco si zařídíte sami.</p>"
             "<p>Dopravu do Vídně a zpět a rezervaci ubytování je nutné provést samostatně – dostanete tipy na vlakovou a autobusovou dopravu "
             "a na různé typy ubytování podle vašeho zadání. Organizační pomoc na místě po příjezdu v rozsahu objednávky je zajištěna.</p>"
             "<p>Další služby, jako doprovod na celodenní výlety v okolí Vídně (zámek, lázeňské město…) nebo rezervace vstupenek, jsou na domluvě. "
             "Program je možné jakkoliv upravovat. Cena se odvíjí od rozsahu služeb, počtu hodin a počtu účastníků.</p>"),
        button("Chci nabídku pro skupinu", KONTAKT, "primary"),
    ], 58),
    column([
        heading("Doprovázela jsem takto již", "h3"),
        icon_list(["Skupinu podnikatelek Ženy z Vysočiny.", "30 studentů Česko-německého gymnázia z Prahy.",
                   "Spolek 50 seniorů z Poděbrad.", "Firmu z Moravy v čele s jejím majitelem a ředitelem."],
                  icon="fas fa-users"),
    ], 42, css="sbz-karta"),
]))

out = ROOT / os.environ.get("SBZ_OUT", "build/viden-podpora.json")
out.write_text(json.dumps(P, ensure_ascii=False, indent=1))
print(f"sections: {len(P)}, testimonials: {len(real)}, images known: {len(images)} -> {out}")
