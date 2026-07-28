import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_layout import build, REGIONS
from extract_corpus import build_corpus_from_folders

# Karte rechnet aus den (lokalen, gitignored) Knotenordnern in Bibliothek/.
BIB = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                    '..', '..', '..', 'Bibliothek', 'Hypnosystemik'))

# Ohne lokales Quellmaterial (z. B. in CI) übersprungen — sonst würde ein leerer
# Corpus die Tests still vakuum-bestehen lassen.
_corpus = build_corpus_from_folders(BIB)
_have_source = sum(len(t.split()) for t in _corpus.values()) > 1000
pytestmark = pytest.mark.skipif(not _have_source,
                                reason="Bibliothek-Quellordner nicht vorhanden (lokal)")


def test_layout_bounds_and_edges():
    L = build(BIB)
    assert len(L["nodes"]) == 50
    for slug, p in L["nodes"].items():
        rx0, rx1, ry0, ry1 = REGIONS[p["cluster"]]
        assert rx0 - 0.01 <= p["x"] <= rx1 + 0.01, (slug, p)
        assert ry0 - 0.01 <= p["y"] <= ry1 + 0.01, (slug, p)
    # Kanten-Vorschläge: cross-cluster, symmetriefrei (a<b), sim absteigend
    clby = {s: p["cluster"] for s, p in L["nodes"].items()}
    for e in L["edges_suggested"]:
        assert clby[e["a"]] != clby[e["b"]], e
        assert e["a"] < e["b"]
    sims = [e["sim"] for e in L["edges_suggested"]]
    assert sims == sorted(sims, reverse=True)
    assert len(L["edges_suggested"]) >= 8


def test_build_is_deterministic():
    a = build(BIB)
    b = build(BIB)
    assert a == b


if __name__ == "__main__":
    test_layout_bounds_and_edges()
    test_build_is_deterministic()
    print("OK test_layout")
