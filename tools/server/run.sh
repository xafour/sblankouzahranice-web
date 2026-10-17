#!/bin/bash
# Použití: run.sh lokalni.php [query]
# Nahraje jednorázový mu-plugin chráněný náhodným tokenem, zavolá ho a hned smaže.
# Přístupové údaje se čtou z ~/.config/xafour/wp_sandbox.env (nejsou v gitu).
D=$(cd "$(dirname "$0")" && pwd); T=$(head -c12 /dev/urandom | od -An -tx1 | tr -d ' \n'); N="zz-claude-$T.php"
TMP=$(mktemp); sed "s/__TOKEN__/$T/" "$1" > "$TMP"
"$D/ftp.sh" "/wp-content/mu-plugins/$N" -T "$TMP" || { rm -f "$TMP"; exit 1; }
rm -f "$TMP"
curl -sS --max-time 600 "${WP_SITE:-https://sandbox.xafour.eu}${WP_PATH:-/}?claude=$T&$2&nc=$RANDOM"
"$D/ftp.sh" "/" -Q "DELE /wp-content/mu-plugins/$N" -o /dev/null
left=$("$D/ftp.sh" "/wp-content/mu-plugins/" --list-only | grep -c zz-claude); [ "$left" = 0 ] || echo "!! mu-plugin zůstal na serveru" >&2
