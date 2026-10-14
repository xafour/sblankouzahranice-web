# sblankouzahranice.eu – redesign

Pracovní repozitář pro optimalizaci a redesign webu sblankouzahranice.eu (sandbox: sandbox.xafour.eu).

- `snapshots/` – exporty dat z WordPressu (nastavení Elementoru = kit, data stránek). Každý commit = stav, ke kterému se dá vrátit.
- `main` = stav webu před redesignem. Redesign se vyvíjí ve větvi `redesign/*`.

Návrat: obnovit data stránky/kitu ze snapshotu v `main` (skript `tools/restore.php` – mu-plugin pro sandbox).
