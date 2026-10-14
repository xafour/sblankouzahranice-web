#!/bin/bash
# Nasadí design systém + jednu stránku (kopii) na sandbox. Použití: tools/deploy.sh <klíč z tools/pages.json>
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SCR=/tmp/claude-1000/-home-xafour-BlankaWeb/a7c5fdff-0dc0-45e4-9321-4249bbee9fec/scratchpad
KEY=${1:?zadej klíč stránky z tools/pages.json}
BUILD=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]]['build'])" "$ROOT/tools/pages.json" "$KEY")
python3 -I "$ROOT/$BUILD"
python3 -I - "$ROOT" "$KEY" "$SCR/remote/claude-payload.json" <<'PY'
import json,sys,pathlib
r=pathlib.Path(sys.argv[1]); cfg=json.loads((r/"tools/pages.json").read_text())[sys.argv[2]]
json.dump({"design":json.loads((r/"design/design-system.json").read_text()),
           "css":(r/"design/sbz.css").read_text(),
           "page":{"slug":cfg["slug"],"title":cfg["title"],"source_id":cfg["source_id"],
                   "elements":json.loads((r/cfg["json"]).read_text())}},
          open(sys.argv[3],"w"),ensure_ascii=False)
PY
"$SCR/tools/ftp.sh" "/wp-content/claude-payload.json" -T "$SCR/remote/claude-payload.json"
"$SCR/tools/run.sh" "$ROOT/tools/deploy-design.php" | grep -v 'widgetType\|^<br />$' | grep -v '^$'
