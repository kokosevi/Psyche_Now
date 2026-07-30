import json, os
import numpy as np
from spaces import SPACE, NODES, out_path
from extract_corpus import build_corpus_from_folders
from tfidf import tfidf_matrix, cosine_dissim
from nmds import nmds

REGIONS = SPACE["regions"]   # x0, x1, y0, y1 je Cluster
CROSS_EDGE_MIN_SIM = SPACE["edges"]["cross_min_sim"]   # Schwelle für Kanten-Vorschläge
CROSS_EDGE_TOPK = SPACE["edges"]["cross_topk"]         # Deckel auf die Vorschlagsliste


MIN_DIST = 6.5   # min. Knotenabstand in % (gegen Label-Überlappung)
TOP_PAD = 6.0    # zusätzlicher Platz oben für den Cluster-Titel


def _fit_region(Y, region):
    """Y (n×2) isotrop in die Region skalieren, zentriert, Aspect erhalten."""
    x0, x1, y0, y1 = region
    y0 = y0 + TOP_PAD  # Knoten nicht unter den Cluster-Titel legen
    if len(Y) == 1:
        return np.array([[(x0 + x1) / 2, (y0 + y1) / 2]])
    Y = Y - Y.mean(axis=0)
    span = np.max(np.abs(Y)) * 2 or 1.0
    w, h = (x1 - x0), (y1 - y0)
    scale = min(w, h) / span * 0.94
    Y = Y * scale
    return Y + np.array([(x0 + x1) / 2, (y0 + y1) / 2])


def _relax(Y, region, min_dist=MIN_DIST, iters=400):
    """Schiebt zu nahe Knotenpaare deterministisch auseinander (Floor auf den
    Abstand), geklemmt in die Region. Bewahrt die NMDS-Anordnung — nur die
    engsten Paare werden entzerrt."""
    x0, x1, y0, y1 = region
    y0 = y0 + TOP_PAD
    Y = Y.astype(float).copy()
    n = len(Y)
    if n < 2:
        return Y
    for _ in range(iters):
        moved = False
        for i in range(n):
            for j in range(i + 1, n):
                d = Y[j] - Y[i]
                dist = float(np.hypot(*d))
                if dist < min_dist:
                    if dist < 1e-9:
                        d = np.array([min_dist, 0.0])  # deterministischer Split
                        dist = min_dist
                    push = (min_dist - dist) / 2.0
                    u = d / dist
                    Y[i] -= u * push
                    Y[j] += u * push
                    moved = True
        Y[:, 0] = np.clip(Y[:, 0], x0, x1)
        Y[:, 1] = np.clip(Y[:, 1], y0, y1)
        if not moved:
            break
    return Y


def build(bib_dir):
    corpus = build_corpus_from_folders(bib_dir)
    slugs = [n["slug"] for n in NODES]
    docs = [corpus[s] for s in slugs]
    mat = tfidf_matrix(docs)                 # globale TF-IDF (ein Vokabular)
    sidx = {s: i for i, s in enumerate(slugs)}
    nodes = {}
    for cl in SPACE["clusters"]:
        members = [n["slug"] for n in NODES if n["cluster"] == cl]
        idx = [sidx[s] for s in members]
        sub = mat[idx]
        D = cosine_dissim(sub)
        Y, _ = nmds(D, seed=42)
        Y = _fit_region(Y, REGIONS[cl])
        Y = _relax(Y, REGIONS[cl])
        for s, (x, y) in zip(members, Y):
            nodes[s] = {"cluster": cl, "x": round(float(x), 2), "y": round(float(y), 2)}
    # Längen-Ausreißer von den Kanten-VORSCHLÄGEN ausschließen (bleiben Knoten):
    # sehr lange Abschnitte (z. B. die 2h-Fallanalyse) sind durch reine Vokabelbreite
    # zu fast allem "ähnlich" → künstlicher Hub. Schwelle: > 4× Median-Wortzahl
    # (trifft nur den Extrem-Ausreißer; zentrale, lange Knoten wie das Netzwerk-Modell
    # bleiben erhalten).
    wc = {s: len(corpus[s].split()) for s in slugs}
    med = sorted(wc.values())[len(wc) // 2]
    excluded = {s for s in slugs if wc[s] > 4 * med}
    if excluded:
        print("Kanten-Ausschluss (Längen-Ausreißer):", ", ".join(sorted(excluded)))
    # Cross-Cluster-Kanten-Vorschläge (die "starken" Verbindungen)
    sim = mat @ mat.T
    edges = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            if nodes[slugs[i]]["cluster"] == nodes[slugs[j]]["cluster"]:
                continue
            if slugs[i] in excluded or slugs[j] in excluded:
                continue
            sc = float(sim[i, j])
            if sc >= CROSS_EDGE_MIN_SIM:
                a, b = sorted((slugs[i], slugs[j]))
                edges.append({"a": a, "b": b, "sim": round(sc, 4)})
    edges.sort(key=lambda e: (-e["sim"], e["a"], e["b"]))
    edges = edges[:CROSS_EDGE_TOPK]
    # Abdeckungs-Set: für JEDEN noch unverbundenen Knoten seine besten
    # cross-cluster-Kandidaten (Top-N) aufnehmen, damit die Kuratierung jedem
    # Knoten ≥1 Kante geben und dabei den Partner mit geringstem Grad wählen
    # kann (verhindert Hubs). Der Längen-Ausreißer bleibt aus der Hub-Bildung
    # heraus (kein Partner für andere), erhält aber selbst seine Partner.
    COVER_TOPN = 3
    def top_partners(i, k):
        cands = []
        for j in range(len(slugs)):
            if j == i or nodes[slugs[i]]["cluster"] == nodes[slugs[j]]["cluster"]:
                continue
            if slugs[j] in excluded and slugs[i] not in excluded:
                continue
            cands.append((slugs[j], float(sim[i, j])))
        cands.sort(key=lambda c: (-c[1], c[0]))
        return cands[:k]
    covered = {e["a"] for e in edges} | {e["b"] for e in edges}
    by_key = {(e["a"], e["b"]): e for e in edges}
    for i, s in enumerate(slugs):
        if s in covered:
            continue
        for partner, sc in top_partners(i, COVER_TOPN):
            a, b = sorted((s, partner))
            by_key.setdefault((a, b), {"a": a, "b": b, "sim": round(sc, 4)})
    merged = sorted(by_key.values(), key=lambda e: (-e["sim"], e["a"], e["b"]))
    return {"nodes": nodes, "edges_suggested": merged}


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    L = build(SPACE["bib_dir"])
    os.makedirs(os.path.join(here, "out"), exist_ok=True)
    layout_p = out_path(here, "layout", "json")
    sugg_p = out_path(here, "edges.suggested", "json")
    json.dump(L["nodes"], open(layout_p, "w"),
              ensure_ascii=False, indent=2, sort_keys=True)
    json.dump(L["edges_suggested"], open(sugg_p, "w"),
              ensure_ascii=False, indent=2)
    print(f"[{SPACE['name']}] {os.path.basename(layout_p)}: {len(L['nodes'])} Knoten; "
          f"{len(L['edges_suggested'])} Kanten-Vorschläge")
