#!/bin/bash
# usage: wp.sh METHOD PATH [curl args...]  — loads creds, strips quotes, never prints them
F=~/.config/xafour/wp_sandbox.env
get(){ grep -E "^$1=" "$F" | head -1 | cut -d= -f2- | sed -E "s/^[\"']//; s/[\"']\s*$//"; }
U=$(get WP_URL); N=$(get WP_USER); P=$(get WP_APP_PASSWORD)
M=$1; shift; PTH=$1; shift
curl -sS -u "$N:$P" -X "$M" "$U/wp-json$PTH" "$@"
