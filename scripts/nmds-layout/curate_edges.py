"""Kuratiert cluster-übergreifende Kanten aus den Ähnlichkeits-Vorschlägen.

Regeln (reproduzierbar):
- Vorschläge nach Ähnlichkeit absteigend (bereits so sortiert).
- Grad-Deckel MAX_DEG pro Knoten → verhindert, dass ein einzelner Knoten
  (z. B. der sehr lange Fallanalyse-Abschnitt) zum Hub wird.
- Mindest-Ähnlichkeit MIN_SIM.
- Garantie: jeder K4-Praxisfall bekommt ≥1 Kante (höchster Vorschlag, notfalls
  über dem Grad-Deckel).
"""
import json, os
from manifest import BY_SLUG

HERE = os.path.dirname(__file__)
MAX_DEG = 3
MIN_SIM = 0.20

sugg = json.load(open(os.path.join(HERE, "out", "edges.suggested.json")))
deg = {}
edges = []


def deg_ok(x):
    return deg.get(x, 0) < MAX_DEG


def add(a, b):
    edges.append(tuple(sorted((a, b))))
    deg[a] = deg.get(a, 0) + 1
    deg[b] = deg.get(b, 0) + 1


chosen = set()
for e in sugg:
    a, b = e["a"], e["b"]
    if e["sim"] < MIN_SIM:
        continue
    if deg_ok(a) and deg_ok(b):
        add(a, b)
        chosen.add(tuple(sorted((a, b))))

# K4-Abdeckung sicherstellen
k4 = [s for s, n in BY_SLUG.items() if n["cluster"] == "k4"]
linked = {x for e in edges for x in e}
for s in k4:
    if s not in linked:
        for e in sugg:
            if s in (e["a"], e["b"]):
                add(e["a"], e["b"])
                linked.add(e["a"])
                linked.add(e["b"])
                break

final = sorted({tuple(sorted(e)) for e in edges})
# Validierung: alle cross-cluster, Slugs existieren
for a, b in final:
    assert a in BY_SLUG and b in BY_SLUG, (a, b)
    assert BY_SLUG[a]["cluster"] != BY_SLUG[b]["cluster"], (a, b)

json.dump([list(e) for e in final],
          open(os.path.join(HERE, "out", "edges.curated.json"), "w"),
          ensure_ascii=False, indent=2)
missing = [s for s in k4 if s not in {x for e in final for x in e}]
print(f"edges.curated.json: {len(final)} Kanten; K4 ohne Kante: {missing or 'keine'}")
print("Grad-Verteilung (Top):", sorted(deg.items(), key=lambda x: -x[1])[:6])
