"""Globales Layout: EINE NMDS über alle 50 Knoten (nicht pro Cluster).

Position = inhaltliche Ähnlichkeit über den gesamten Korpus (TF-IDF-Kosinus).
Cluster-Zugehörigkeit steckt nur noch in der Farbe, nicht mehr in der Region.
Output: out/layout.global.json = { slug: {x, y} } und Kopie nach site/src/lib/.
"""
import json, os
import numpy as np
from manifest import NODES
from extract_corpus import build_corpus
from tfidf import tfidf_matrix, cosine_dissim
from nmds import nmds

HERE = os.path.dirname(__file__)
CANVAS = (5, 95, 6, 94)   # x0, x1, y0, y1 (fast volle Bühne)
MIN_DIST = 6.0            # min. Knotenabstand in %


def _fit(Y, region):
    x0, x1, y0, y1 = region
    Y = Y - Y.mean(axis=0)
    span = np.max(np.abs(Y)) * 2 or 1.0
    scale = min(x1 - x0, y1 - y0) / span * 0.96
    return Y * scale + np.array([(x0 + x1) / 2, (y0 + y1) / 2])


def _relax(Y, region, min_dist=MIN_DIST, iters=500):
    x0, x1, y0, y1 = region
    Y = Y.astype(float).copy()
    n = len(Y)
    for _ in range(iters):
        moved = False
        for i in range(n):
            for j in range(i + 1, n):
                d = Y[j] - Y[i]
                dist = float(np.hypot(*d))
                if dist < min_dist:
                    if dist < 1e-9:
                        d = np.array([min_dist, 0.0]); dist = min_dist
                    push = (min_dist - dist) / 2.0
                    u = d / dist
                    Y[i] -= u * push; Y[j] += u * push
                    moved = True
        Y[:, 0] = np.clip(Y[:, 0], x0, x1)
        Y[:, 1] = np.clip(Y[:, 1], y0, y1)
        if not moved:
            break
    return Y


def build_global(doc_path):
    corpus = build_corpus(doc_path)
    slugs = [n["slug"] for n in NODES]
    mat = tfidf_matrix([corpus[s] for s in slugs])
    D = cosine_dissim(mat)
    Y, stress = nmds(D, seed=42)
    Y = _fit(Y, CANVAS)
    Y = _relax(Y, CANVAS)
    layout = {s: {"x": round(float(x), 2), "y": round(float(y), 2)}
              for s, (x, y) in zip(slugs, Y)}
    return layout, stress


if __name__ == "__main__":
    doc = os.path.join(HERE, "source", "doc.txt")
    layout, stress = build_global(doc)
    out = os.path.join(HERE, "out", "layout.global.json")
    json.dump(layout, open(out, "w"), ensure_ascii=False, indent=2, sort_keys=True)
    site_copy = os.path.normpath(os.path.join(HERE, "..", "..", "site", "src", "lib", "layout.global.json"))
    json.dump(layout, open(site_copy, "w"), ensure_ascii=False, indent=2, sort_keys=True)
    print(f"layout.global.json: {len(layout)} Knoten; NMDS-Stress={stress:.3f}")
