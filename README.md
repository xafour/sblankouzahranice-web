# Web „s Blankou za hranice“ – sblankouzahranice.eu

Pracovní repozitář pro úpravy a redesign webu **[sblankouzahranice.eu](https://sblankouzahranice.eu)**.
Všechno se nejdřív zkouší na zkušební kopii **[sandbox.xafour.eu](https://sandbox.xafour.eu)** (skrytá před Googlem), živý web se mění až po schválení.

👉 **Blanko, začněte tady: [PRUVODCE.md](PRUVODCE.md)** – co je git a GitHub a jak tu číst změny.

💡 **Návrhy, co dalšího zlepšit, a varianty vzhledu: [navrhy/NAVRHY.md](navrhy/NAVRHY.md)**

## Co tu je

| Složka | Co obsahuje |
|---|---|
| [`web/`](web/README.md) | Obsah webu: všechny stránky, články a šablony (data Elementoru + čitelné texty), menu, seznam pluginů, nastavení šablony Kadence |
| `snapshots/` | Přesné zálohy dat stránek, na kterých stavíme redesign |
| `design/` | Nový design systém (barvy, písma, CSS) – jen ve větvích `redesign/*` |
| `build/`, `tools/` | Skripty, které stránky v novém designu sestaví a nahrají na sandbox |

## Větve (branches)

| Větev | Co v ní je |
|---|---|
| `main` | Web tak, jak je dnes (výchozí stav před redesignem) |
| `redesign/design-system` | Nové barvy a písma + první stránka v novém designu |
| `redesign/dalsi-stranky` | Další stránky v novém designu |
| `navrhy/optimalizace` | Návrhy, co dalšího jde zlepšit, a varianty k výběru |

## Co v repozitáři záměrně NENÍ

Repozitář je veřejný, proto tu nejsou: databáze (komentáře, uživatelé, formuláře zákazníků), hesla a přístupy,
zálohy `.wpress`, fotky (jsou na webu; 328 MB), placené pluginy ani statistiky návštěvnosti.
Cílová e-mailová adresa formulářů je v exportu nahrazena `skryty-email@example.invalid`.

## Technicky

- Export obsahu: `tools/server/run.sh tools/server/export-all.php > export.json && python3 tools/export_web.py export.json`
  (přístupy k sandboxu se čtou z `~/.config/xafour/wp_sandbox.env`, nejsou v gitu).
- Nasazení stránky v novém designu: `tools/deploy.sh <klíč>` (klíče v `tools/pages.json`, stavební prvky v `tools/sbz.py`).
- Návrat redesignu: `tools/rollback-design.php` odebere nové globální styly `sbz_*`, CSS blok a kopie stránek. Původní stránky redesign nemění.
