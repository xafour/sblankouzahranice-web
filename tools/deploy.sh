#!/bin/bash
# Nasadí design systém + stránku na sandbox. Použití: tools/deploy.sh
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SCR=/tmp/claude-1000/-home-xafour-BlankaWeb/a7c5fdff-0dc0-45e4-9321-4249bbee9fec/scratchpad
python3 -I "$ROOT/tools/build_viden_podpora.py"
python3 -I - "$ROOT" "$SCR/remote/claude-payload.json" <<'PY'
import json,sys,pathlib
r=pathlib.Path(sys.argv[1])
json.dump({"design":json.loads((r/"design/design-system.json").read_text()),
           "css":(r/"design/sbz.css").read_text(),
           "page":{"slug":"viden-cestovni-podpora-novy-design","title":"Vídeň – individuální cestovní podpora (nový design)",
                   "source_id":19575,"elements":json.loads((r/"build/viden-podpora.json").read_text())}},
          open(sys.argv[2],"w"),ensure_ascii=False)
PY
"$SCR/tools/ftp.sh" "/wp-content/claude-payload.json" -T "$SCR/remote/claude-payload.json"
"$SCR/tools/run.sh" "$ROOT/tools/deploy-design.php"
