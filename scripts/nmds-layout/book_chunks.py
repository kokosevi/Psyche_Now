"""Zerlegt extrahierten Buchtext in Kapitel-Chunks (Retrieval-Einheit).
Überschrift = Zeilenanfang 'N[.N…] Titel' (Ziffern-Nummerierung, Titel nicht leer)."""
import os, re, glob

_HEAD = re.compile(r'^(\d+(?:\.\d+)*)\s+(\S.*\S|\S)\s*$')


def _is_heading(num, title):
    """Validate that a matched num/title line is a genuine heading, not a PDF artifact.

    Rejects:
    - Any num segment with leading zero (00, 01) → kills page footers
    - Any num segment with ≥4 digits (2014) → kills year segments
    - More than 4 dot-levels → structure sanity
    - Title with ':' → kills timestamps like "14:59:54"
    - Title with '.indb' → kills page footer text
    - Title ending with '.', ',', ';' → kills digit-led sentences and references
    """
    # Check num segments
    segments = num.split('.')
    if len(segments) > 4:
        return False
    for seg in segments:
        if seg[0] == '0':  # Leading zero
            return False
        if len(seg) >= 4:  # ≥4 digits (kills years)
            return False

    # Check title
    if ':' in title:  # Kills timestamps
        return False
    if '.indb' in title.lower():  # Kills page footers
        return False
    if title and title[-1] in '.;,':  # Kills digit-led sentences, references
        return False

    return True


def chapters(text):
    lines = text.split("\n")
    heads = []  # (line_index, num, title)
    for i, l in enumerate(lines):
        m = _HEAD.match(l)
        if m:
            num, title = m.group(1), m.group(2).strip()
            if _is_heading(num, title):  # Filter out artifacts
                heads.append((i, num, title))
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
