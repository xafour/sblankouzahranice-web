#!/bin/bash
# usage: ftp.sh REMOTE_PATH [curl args...]   (FTPS explicit TLS; creds never printed)
F=~/.config/xafour/wp_sandbox.env
get(){ grep -E "^$1=" "$F" | head -1 | cut -d= -f2- | sed -E "s/^[\"']//; s/[\"']\s*$//; s/\r$//"; }
H=$(get FTP_HOST); H=${H#ftp://}; H=${H%/}
R=$1; shift
curl -sS --ssl-reqd --netrc-file <(printf 'machine %s login %s password %s\n' "$H" "$(get FTP_USER)" "$(get FTP_PASSWORD)") "ftp://$H$R" "$@"
