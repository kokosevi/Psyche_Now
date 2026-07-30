"""Ordnet jedem Konzept die passenden Kapitel-Chunks zu und schreibt die
Knotenordner (quelle.md + meta.json). quelle.md bleibt lokal (gitignored)."""
import os, re, json


def _count(term, text):
    return len(re.findall(re.escape(term.lower()), text.lower()))


def score_chunks(terms, chunks):
    out = []
    for i, c in enumerate(chunks):
        words = max(1, len(c["text"].split()))
        raw = sum(_count(t, c["text"]) for t in terms)
        out.append((i, raw / words * 1000.0))
    out.sort(key=lambda p: (-p[1], p[0]))
    return out


def retrieve(nodes, chunks, top_k=6):
    assign = {}
    for nd in nodes:
        ranked = [(i, s) for i, s in score_chunks(nd["terms"], chunks) if s > 0]
        assign[nd["slug"]] = [i for i, _ in ranked[:top_k]]
    return assign


def write_folders(bib_dir, nodes, chunks, assign):
    from extract_corpus import folder_name
    written = 0
    for nd in nodes:
        d = os.path.join(bib_dir, folder_name(nd))
        os.makedirs(d, exist_ok=True)
        idxs = assign[nd["slug"]]
        body = "\n\n".join(f"## {chunks[i]['book']} — Passage {i}\n{chunks[i]['text']}"
                           for i in idxs)
        open(os.path.join(d, "quelle.md"), "w", encoding="utf-8").write(body)
        meta = {"title": nd["title"],
                "summary": f"TODO: eigene Zusammenfassung zu «{nd['title']}».",
                "status": "stub"}
        json.dump(meta, open(os.path.join(d, "meta.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        written += 1
    return written


if __name__ == "__main__":
    from psyche_manifest import NODES
    from book_chunks import all_passages
    HERE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
    ext = os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie Materials", "_extracted")
    bib = os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie")
    chunks = all_passages(ext)
    assign = retrieve(NODES, chunks)
    n = write_folders(bib, NODES, chunks, assign)
    empty = [s for s, v in assign.items() if not v]
    print(f"{n} Knotenordner geschrieben; ohne Treffer: {empty or 'keine'}")
