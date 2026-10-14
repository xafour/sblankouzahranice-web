# sblankouzahranice.eu – redesign

Pracovní repozitář pro optimalizaci a redesign webu sblankouzahranice.eu (sandbox: sandbox.xafour.eu).

- `snapshots/` – exporty dat z WordPressu (nastavení Elementoru = kit, data stránek). Každý commit = stav, ke kterému se dá vrátit.
- `main` = stav webu před redesignem. Redesign se vyvíjí ve větvi `redesign/*`.

Nasazení: `tools/deploy.sh <klíč>` – klíče stránek jsou v `tools/pages.json`; stavební prvky jsou v `tools/sbz.py`.
Návrat: `tools/rollback-design.php` – odebere nové globální styly sbz_*, CSS blok a kopii stránky. Původní stránky redesign nemění.
