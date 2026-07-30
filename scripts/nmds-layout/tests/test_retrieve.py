import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from retrieve_passages import score_chunks, retrieve

CHUNKS = [
    {"text": "Der Sollwert steuert den Regelkreis. Sollwert überall.", "book": "b"},
    {"text": "Farbe und Form der Wahrnehmung.", "book": "b"},
    {"text": "Ein Satz ohne Treffer hier.", "book": "b"},
]


def test_score_normiert():
    sc = dict(score_chunks(["sollwert", "regelkreis"], CHUNKS))
    assert sc[0] > sc[1], sc          # Chunk 0 trifft, Chunk 1 nicht
    assert sc[2] == 0.0


def test_retrieve_top_k_nur_positive():
    nodes = [{"slug": "x", "terms": ["sollwert"]}, {"slug": "y", "terms": ["nichttreffer"]}]
    a = retrieve(nodes, CHUNKS, top_k=2)
    assert a["x"] == [0]               # nur Chunk 0 hat Score>0
    assert a["y"] == []                # kein Treffer -> leer


if __name__ == "__main__":
    test_score_normiert()
    test_retrieve_top_k_nur_positive()
    print("OK test_retrieve")
