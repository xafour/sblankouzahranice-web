# Průvodce pro Blanku: git a GitHub

Tento repozitář založil Milan. Chtěl vám ukázat způsob práce, který používají programátoři:
**každá změna webu je zapsaná, popsaná a dá se kdykoli vrátit.**

## Co je git

Představte si sešit, do kterého se automaticky zapisuje každá úprava webu:
*„15. 10. – změněný nadpis na stránce Vídeň – cestovní podpora, původně ‚Chystáte se DO VÍDNĚ?‘, nově …“*.

- Každý takový zápis se jmenuje **commit**. Má datum, autora a popis, co a proč se změnilo.
- Z kteréhokoli commitu se dá web vrátit do tehdejšího stavu.

## Co je GitHub

GitHub je web, kde je tento „sešit“ uložený a dá se pohodlně prohlížet v prohlížeči:
**https://github.com/xafour/sblankouzahranice-web**

Nemusíte nic instalovat ani se registrovat, všechno si můžete prohlížet.

## Co jsou větve (branches)

Větev je **samostatná pracovní verze**, ve které se dá zkoušet bez rizika. Je to jako kopie sešitu „na zkoušku“.

- `main` = **web tak, jak je dnes**. Na tuhle větev se nesahá, dokud změny neschválíte.
- `redesign/design-system` = nové barvy, písma a první stránka v novém designu.
- `redesign/dalsi-stranky` = další stránky v novém designu.
- `navrhy/optimalizace` = návrhy, co dalšího jde zlepšit, a varianty, ze kterých si můžete vybrat.

Když se vám něco líbí, větev se **sloučí** (*merge*) do `main` a teprve potom jde na živý web.
Když se vám nelíbí, větev se prostě zahodí a web zůstane, jak byl.

## Jak si prohlédnout změny na GitHubu

1. Otevřete https://github.com/xafour/sblankouzahranice-web
2. Vlevo nahoře je přepínač s nápisem **`main`**. Klikněte a vyberte jinou větev.
3. Odkaz **„commits“** (ikonka hodin) ukáže historii: kdo, kdy a co změnil.
   Po kliknutí na commit uvidíte změny: **červeně** je, co se smazalo, **zeleně**, co přibylo.
4. Porovnání celé větve s dneškem: v adrese doplňte `/compare/main...navrhy/optimalizace`.
5. Texty všech stránek jsou ve složce **[`web/texty/`](web/texty/)** jako obyčejný text.
   Když se změní text na stránce, v historii přesně uvidíte které slovo.

## Proč je to dobré

| Bez gitu | S gitem |
|---|---|
| „Kdy jsem to změnila a jak to bylo předtím?“ | Každá změna je zapsaná s datem a popisem. |
| Zkoušení přímo na živém webu, kde to vidí zákazníci | Zkouší se na sandboxu a ve větvi, živý web se nemění. |
| Když se něco rozbije, obnovuje se celá záloha (a ztratí se i dobré změny) | Vrátí se jen ta jedna změna. |
| Na webu pracuje víc lidí (vy, Milan, Claude) a nikdo neví, co dělal ten druhý | Historie ukazuje, kdo co udělal. |

## Co tu záměrně není

Repozitář je **veřejný** (může ho vidět kdokoli). Proto tu **nejsou** hesla, databáze s komentáři a údaji zákazníků,
zálohy webu, fotky ani statistiky návštěvnosti. Jsou tu jen texty a nastavení, které jsou stejně vidět na webu.

## Jak s tím můžete pracovat vy

Nic se nemusíte učit. Stačí napsat Claudovi do okna terminálu na Milanově počítači, třeba:

- *„Ukaž mi, co se změnilo na stránce Den ve Vídni.“*
- *„Ten nový nadpis se mi nelíbí, vrať tam můj původní.“*
- *„Udělej variantu úvodní stránky s tmavší zelenou.“*
- *„Co ještě by se dalo na webu zlepšit?“*

Claude změnu udělá na sandboxu, zapíše ji do gitu jako commit a pošle na GitHub. Vy se podíváte a rozhodnete.
