import json, os
import numpy as np
from manifest import NODES
from extract_corpus import build_corpus
from tfidf import tfidf_matrix, cosine_dissim
from nmds import nmds

REGIONS = {  # x0, x1, y0, y1
    "k1": (6, 46, 8, 46), "k2": (54, 94, 8, 46),
    "k3": (6, 46, 54, 92), "k4": (54, 94, 54, 92),
}
CROSS_EDGE_MIN_SIM = 0.10   # Schwelle für Kanten-Vorschläge
CROSS_EDGE_TOPK = 40        # Deckel auf die Vorschlagsliste


def _fit_region(Y, region):
    """Y (n×2) isotrop in die Region skalieren, zentriert, Aspect erhalten."""
    x0, x1, y0, y1 = region
    if len(Y) == 1:
        return np.array([[(x0 + x1) / 2, (y0 + y1) / 2]])
    Y = Y - Y.mean(axis=0)
    span = np.max(np.abs(Y)) * 2 or 1.0
    w, h = (x1 - x0), (y1 - y0)
    scale = min(w, h) / span * 0.92
    Y = Y * scale
    return Y + np.array([(x0 + x1) / 2, (y0 + y1) / 2])


def build(doc_path):
    corpus = build_corpus(doc_path)
    slugs = [n["slug"] for n in NODES]
    docs = [corpus[s] for s in slugs]
    mat = tfidf_matrix(docs)                 # globale TF-IDF (ein Vokabular)
    sidx = {s: i for i, s in enumerate(slugs)}
    nodes = {}
    for cl in ("k1", "k2", "k3", "k4"):
        members = [n["slug"] for n in NODES if n["cluster"] == cl]
        idx = [sidx[s] for s in members]
        sub = mat[idx]
        D = cosine_dissim(sub)
        Y, _ = nmds(D, seed=42)
        Y = _fit_region(Y, REGIONS[cl])
        for s, (x, y) in zip(members, Y):
            nodes[s] = {"cluster": cl, "x": round(float(x), 2), "y": round(float(y), 2)}
    # Cross-Cluster-Kanten-Vorschläge
    sim = mat @ mat.T
    edges = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            if nodes[slugs[i]]["cluster"] == nodes[slugs[j]]["cluster"]:
                continue
            sc = float(sim[i, j])
            if sc >= CROSS_EDGE_MIN_SIM:
                a, b = sorted((slugs[i], slugs[j]))
                edges.append({"a": a, "b": b, "sim": round(sc, 4)})
    edges.sort(key=lambda e: (-e["sim"], e["a"], e["b"]))
    edges = edges[:CROSS_EDGE_TOPK]
    return {"nodes": nodes, "edges_suggested": edges}


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    doc = os.path.join(here, "source", "doc.txt")
    L = build(doc)
    os.makedirs(os.path.join(here, "out"), exist_ok=True)
    json.dump(L["nodes"], open(os.path.join(here, "out", "layout.json"), "w"),
              ensure_ascii=False, indent=2, sort_keys=True)
    json.dump(L["edges_suggested"], open(os.path.join(here, "out", "edges.suggested.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"layout.json: {len(L['nodes'])} Knoten; {len(L['edges_suggested'])} Kanten-Vorschläge")
