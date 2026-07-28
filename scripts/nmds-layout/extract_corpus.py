import re
from manifest import NODES

_HDR = re.compile(r'^(#{2,3})\s+(\d+(?:\.\d+){0,3})\.?\s+(.*)$')


def _sections(doc_path):
    """Liste (num_key, title, body) für jede ## / ### Überschrift im Body."""
    lines = open(doc_path, encoding="utf-8").read().split("\n")
    heads = []  # (line_index, level, num, title)
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith('[') and 'docs.google' in s:
            continue  # TOC überspringen
        m = _HDR.match(s)
        if m:
            heads.append((i, len(m.group(1)), m.group(2), m.group(3)))
    out = []
    for idx, (li, lvl, num, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        body = "\n".join(lines[li + 1:end]).strip()
        out.append((num, title, body))
    return out


def _key_for(num, title):
    """Erzeugt den heading-key inkl. 1.3-Disambiguierung."""
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
