import re
from manifest import NODES

# Format der Quelle (Life Lessons - Transkripte.txt):
# Abschnitte sind mit Separatorlinien (----- / =====) umrahmt; die Überschrift ist
# eine nicht-eingerückte Zeile "N[.N…] Titel (mm:ss)" direkt nach einem Separator.
# Das TOC am Dateianfang ist eingerückt und NICHT separator-umrahmt → wird ignoriert.
_SEP = re.compile(r'^[-=]{5,}\s*$')
_BND = re.compile(r'^(\d+(?:\.\d+)*)\.?\s+(.*\S)\s*$')  # Kapitel- oder Unterkapitel-Überschrift


def _sections(doc_path):
    """Liste (num_key, title, body) für jede separator-umrahmte Unterkapitel-Überschrift."""
    lines = open(doc_path, encoding="utf-8").read().split("\n")
    bounds = []  # (line_index, num, title) — alle Kapitel-/Unterkapitel-Grenzen
    for i, l in enumerate(lines):
        m = _BND.match(l)
        if not m:
            continue
        k = i - 1
        while k >= 0 and lines[k].strip() == "":
            k -= 1
        if k >= 0 and _SEP.match(lines[k]):
            bounds.append((i, m.group(1), m.group(2)))
    out = []
    for idx, (li, num, title) in enumerate(bounds):
        end = bounds[idx + 1][0] if idx + 1 < len(bounds) else len(lines)
        if "." not in num:
            continue  # reiner Kapitel-Header (z. B. "1"/"2") — kein Knoten
        body_lines = [x for x in lines[li + 1:end] if not _SEP.match(x)]
        out.append((num, title, "\n".join(body_lines).strip()))
    return out


def _key_for(num, title):
    """Erzeugt den heading-key inkl. 1.3-Disambiguierung (Sag mal / Werdegang)."""
    if num == "1.3":
        if "Sag mal" in title:
            return "1.3s"
        if "Werdegang" in title:
            return "1.3w"
    return num


def build_corpus(doc_path):
    secs = _sections(doc_path)
    by_key = {}
    for num, title, body in secs:
        by_key[_key_for(num, title)] = body
    corpus = {}
    for nd in NODES:
        parts = [by_key.get(k, "") for k in nd["headings"]]
        corpus[nd["slug"]] = "\n".join(p for p in parts if p).strip()
    return corpus
