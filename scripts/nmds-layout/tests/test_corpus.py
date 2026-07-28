import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from manifest import NODES
from extract_corpus import build_corpus

DOC = os.path.join(os.path.dirname(__file__), '..', 'source', 'doc.txt')


def test_manifest_shape():
    assert len(NODES) == 50, f"expected 50 nodes, got {len(NODES)}"
    clusters = {}
    for nd in NODES:
        clusters.setdefault(nd["cluster"], 0)
        clusters[nd["cluster"]] += 1
    assert clusters == {"k1": 15, "k2": 10, "k3": 17, "k4": 8}, clusters
    slugs = [nd["slug"] for nd in NODES]
    assert len(set(slugs)) == 50, "slugs not unique"


def test_corpus_covers_every_node_with_text():
    corpus = build_corpus(DOC)
    assert set(corpus.keys()) == {nd["slug"] for nd in NODES}
    for slug, text in corpus.items():
        assert len(text.split()) >= 40, f"{slug} too short: {len(text.split())} words"


if __name__ == "__main__":
    test_manifest_shape()
    test_corpus_covers_every_node_with_text()
    print("OK test_corpus")
