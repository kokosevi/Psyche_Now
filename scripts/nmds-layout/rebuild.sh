#!/usr/bin/env bash
# Rebuild einer Karte (Distanzen + Kanten) UND des veröffentlichten Contents aus den
# Knotenordnern in Bibliothek/<Raum>/<seq>-<slug>/.
# Nach jeder Änderung an quelle.md / text.md / meta.json / Bildern hier ausführen.
#
# Aufruf:  ./rebuild.sh [raum]   (raum = erleben | herausforderungen; Default erleben)
set -euo pipefail
cd "$(dirname "$0")"
export SPACE="${1:-erleben}"
PY="./.venv/bin/python"
[ -x "$PY" ] || PY="python3"
echo "▶ Raum: $SPACE"
echo "→ build_layout (NMDS-Positionen + Kantenvorschläge aus den Ordnern)"
"$PY" build_layout.py
echo "→ curate_edges (Kanten kuratieren, jeder Knoten ≥1 Kante)"
"$PY" curate_edges.py
echo "→ sync_content (index.md + Medien nach site/src/content/<collection>/)"
"$PY" sync_content.py
echo "✓ fertig. Danach: cd site && npm run build"
