"""Zerlegt extrahierten Buchtext in Kapitel-Chunks (Retrieval-Einheit).
Überschrift = Zeilenanfang 'N[.N…] Titel' (Ziffern-Nummerierung, Titel nicht leer)."""
import os, re, glob

_HEAD = re.compile(r'^(\d+(?:\.\d+)*)\s+(\S.*\S|\S)\s*$')


def chapters(text):
    lines = text.split("\n")
    heads = []  # (line_index, num, title)
    for i, l in enumerate(lines):
        m = _HEAD.match(l)
        if m:
            heads.append((i, m.group(1), m.group(2).strip()))
    out = []
    for idx, (li, num, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        body = "\n".join(lines[li + 1:end]).strip()
        out.append({"num": num, "title": title, "text": body})
    return out


def all_chunks(extracted_dir):
    out = []
    for path in sorted(glob.glob(os.path.join(extracted_dir, "*.txt"))):
        book = os.path.splitext(os.path.basename(path))[0]
        for c in chapters(open(path, encoding="utf-8").read()):
            out.append({**c, "book": book})
    return out
