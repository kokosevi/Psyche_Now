#!/usr/bin/env bash
# Rebuild: Erleben-Karte (Distanzen + Kanten) UND veröffentlichter Content aus den
# Knotenordnern in Bibliothek/Hypnosystemik/<nummer>-<slug>/.
# Nach jeder Änderung an quelle.md / text.md / meta.json / Bildern hier ausführen.
set -euo pipefail
cd "$(dirname "$0")"
PY="./.venv/bin/python"
[ -x "$PY" ] || PY="python3"
echo "→ build_layout (NMDS-Positionen + Kantenvorschläge aus den Ordnern)"
"$PY" build_layout.py
echo "→ curate_edges (Kanten kuratieren, jeder Knoten ≥1 Kante)"
"$PY" curate_edges.py
echo "→ sync_content (index.md + Medien nach site/src/content/themen/)"
"$PY" sync_content.py
echo "✓ fertig. Danach: cd site && npm run build"
