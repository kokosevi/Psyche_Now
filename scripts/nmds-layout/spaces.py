"""Raum-Konfiguration: „Erleben" (Hypnosystemik) und „Herausforderungen"
koexistieren als zwei unabhängige Karten.

Der aktive Raum wird über die Env-Var SPACE gewählt (Default: 'erleben').
Ohne SPACE bleibt das Erleben-Verhalten unverändert (gleiche Knoten, Regionen,
Ausgabedateien) — der Determinismus (seed=42) und die Idempotenz gelten weiter.

Jeder Raum liefert:
  name        Raumname
  bib_dir     Quelle: Bibliothek/<...>/<seq>-<slug>/ (quelle.md, text.md, meta.json)
  themen_dir  Ziel:   site/src/content/<collection>/<slug>/index.md
  nodes       Knotenliste [{slug, cluster, headings, title}]
  clusters    Cluster-IDs in Zeichen-Reihenfolge (Quadranten)
  regions     Cluster-ID -> (x0, x1, y0, y1) Layout-Region in %
  out_suffix  Suffix der Zwischen-Dateien in out/ ('' = Erleben, byte-kompatibel)
"""
import math
import os
from manifest import NODES as _ERLEBEN_NODES

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

# Vier Quadranten-Regionen (x0, x1, y0, y1).
# Parameter: mx/my = Außenrand, gx/gy = Lücke zwischen den Rechtecken (in %).
# Kleinere Ränder + kleinere Lücke => größere, näher beieinander liegende Rechtecke.
def _quadrants(a, b, c, d, mx=6, my=8, gx=8, gy=8):
    xl0, xl1 = mx, 50 - gx / 2
    xr0, xr1 = 50 + gx / 2, 100 - mx
    yt0, yt1 = my, 50 - gy / 2
    yb0, yb1 = 50 + gy / 2, 100 - my
    return {a: (xl0, xl1, yt0, yt1), b: (xr0, xr1, yt0, yt1),
            c: (xl0, xl1, yb0, yb1), d: (xr0, xr1, yb0, yb1)}


# Defaults reproduzieren die bisherigen Werte (byte-identisch für Herausforderungen).
_QUADRANTS = lambda a, b, c, d: _quadrants(a, b, c, d)


def _grid_regions(ids, cols=3):
    """Gleichmäßiges Grid im Canvas [5,95]² mit kleiner Lücke zwischen den Zellen."""
    n = len(ids)
    rows = math.ceil(n / cols)
    gap = 2.0
    cw = (90.0 - gap * (cols - 1)) / cols
    ch = (90.0 - gap * (rows - 1)) / rows
    out = {}
    for k, cid in enumerate(ids):
        r, c = divmod(k, cols)
        x0 = 5.0 + c * (cw + gap)
        y0 = 5.0 + r * (ch + gap)
        out[cid] = (round(x0, 2), round(x0 + cw, 2), round(y0, 2), round(y0 + ch, 2))
    return out

# Kanten-Parameter je Raum. Erleben-Werte = die bisherigen Konstanten (byte-identisch).
# Herausforderungen: die kurzen Steckbriefe liefern deutlich kleinere TF-IDF-Cosinus
# (max ~0.10 statt >0.20), daher niedrigere Schwellen und ein höherer Grad-Deckel für
# eine ähnlich dichte Konstellation.
_EDGES_ERLEBEN = {"cross_min_sim": 0.10, "cross_topk": 40, "curate_min_sim": 0.20, "curate_max_deg": 3}
_EDGES_HERAUS = {"cross_min_sim": 0.04, "cross_topk": 80, "curate_min_sim": 0.05, "curate_max_deg": 4}
# Psyche: ~50-Knoten-Karte wie Erleben, daher zunächst dieselben Schwellen
# (bei Bedarf später anhand der tatsächlichen TF-IDF-Verteilung nachjustieren).
_EDGES_PSYCHE = {"cross_min_sim": 0.10, "cross_topk": 40, "curate_min_sim": 0.20, "curate_max_deg": 3}

_ERLEBEN = {
    "name": "erleben",
    "bib_dir": os.path.join(ROOT, "Bibliothek", "Hypnosystemik"),
    "themen_dir": os.path.join(ROOT, "site", "src", "content", "themen"),
    "nodes": _ERLEBEN_NODES,
    "clusters": ("k1", "k2", "k3", "k4"),
    # Kompaktere Karte: große Außenränder ziehen die Cluster zur Mitte, kleine
    # Lücke dazwischen -> deutlich weniger Leerraum zwischen den Rechtecken.
    "regions": _quadrants("k1", "k2", "k3", "k4", mx=15, my=15, gx=6, gy=6),
    "out_suffix": "",
    "edges": _EDGES_ERLEBEN,
}


def _herausforderungen():
    # Knotenliste wird in Phase 3 nach heraus_manifest.py generiert; bis dahin leer.
    try:
        from heraus_manifest import NODES as _HN
    except Exception:
        _HN = []
    return {
        "name": "herausforderungen",
        "bib_dir": os.path.join(ROOT, "Bibliothek", "Herausforderungen"),
        "themen_dir": os.path.join(ROOT, "site", "src", "content", "herausforderungen"),
        "nodes": _HN,
        "clusters": ("h1", "h2", "h3", "h4"),
        "regions": _QUADRANTS("h1", "h2", "h3", "h4"),
        "out_suffix": ".herausforderungen",
        "edges": _EDGES_HERAUS,
    }


_PSYCHE_CLUSTERS = ("p1", "p2", "p3", "p4", "p5")


def _psyche():
    try:
        from psyche_manifest import NODES as _PN
    except Exception:
        _PN = []
    return {
        "name": "psyche",
        "bib_dir": os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie"),
        "themen_dir": os.path.join(ROOT, "site", "src", "content", "psyche"),
        "nodes": _PN,
        "clusters": _PSYCHE_CLUSTERS,
        "regions": _grid_regions(_PSYCHE_CLUSTERS, cols=3),
        "out_suffix": ".psyche",
        "edges": _EDGES_PSYCHE,
    }


def get_space(name=None):
    name = name or os.environ.get("SPACE", "erleben")
    if name == "erleben":
        return _ERLEBEN
    if name == "herausforderungen":
        return _herausforderungen()
    if name == "psyche":
        return _psyche()
    raise SystemExit(f"Unbekannter SPACE: {name!r} (erlaubt: erleben | herausforderungen | psyche)")


SPACE = get_space()
NODES = SPACE["nodes"]
BY_SLUG = {n["slug"]: n for n in NODES}


def out_path(here, base, ext):
    """out/<base><suffix>.<ext> — Suffix je Raum ('' für Erleben)."""
    return os.path.join(here, "out", f"{base}{SPACE['out_suffix']}.{ext}")
