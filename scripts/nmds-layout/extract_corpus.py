import os, re, glob
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


# --- Ordner-basierter Corpus (aktuelle Quelle für die Karte) -----------------
# Jeder Knoten hat einen Ordner Bibliothek/Hypnosystemik/<nummer>-<slug>/ mit
# beliebig vielen *.md (quelle.md, text.md …). Der Corpus eines Knotens ist die
# Konkatenation ALLER *.md in seinem Ordner. Ändert sich der Ordnerinhalt, ändert
# sich die Karte.

def toc_number(node):
    """TOC-Nummer eines Knotens (Buchstaben-Suffix entfernt, erste bei mehreren)."""
    return re.sub(r"[a-z]+$", "", node["headings"][0])


def folder_name(node):
    return f"{toc_number(node)}-{node['slug']}"


def build_corpus_from_folders(bib_dir):
    """{slug: text} — alle *.md je Knotenordner konkateniert."""
    corpus = {}
    for nd in NODES:
        d = os.path.join(bib_dir, folder_name(nd))
        texts = []
        for path in sorted(glob.glob(os.path.join(d, "*.md"))):
            texts.append(open(path, encoding="utf-8").read())
        corpus[nd["slug"]] = "\n".join(texts).strip()
    return corpus
