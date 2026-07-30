"""Zerlegt extrahierten Buchtext in Passagen-Fenster (~target_words) an
Absatzgrenzen — die Retrieval-Einheit für die Konzept-Zuordnung.
Seiten-Möblierung (Export-Timestamp, .indb-Footer, reine Seitenzahlen,
Form-Feed) wird vor dem Fenstern entfernt, damit sie den TF-IDF-Corpus nicht
verrauscht."""
import os, re, glob

# Pro Seite wiederkehrendes Rauschen aus dem PDF-Export.
_NOISE = [
    re.compile(r'^\s*\d{1,2}\.\d{1,2}\.\d{4}\s+\d{1,2}:\d{2}(:\d{2})?\s*$'),  # 13.01.2014 14:59:54
    re.compile(r'\.indb\b'),                                                  # …indb 123 Footer
    re.compile(r'^\s*\d{1,4}\s*$'),                                           # reine Seitenzahl
    re.compile(r'^\s*\f\s*$'),                                                # Form-Feed
]


def _clean_lines(text):
    for raw in text.replace("\f", "\n").split("\n"):
        if any(p.search(raw) for p in _NOISE):
            continue
        yield raw


def _paragraphs(text):
    para, buf = [], []
    for line in _clean_lines(text):
        if line.strip():
            buf.append(line.strip())
        elif buf:
            para.append(" ".join(buf)); buf = []
    if buf:
        para.append(" ".join(buf))
    return para


def passages(text, target_words=200):
    out, buf, wc = [], [], 0
    for p in _paragraphs(text):
        buf.append(p); wc += len(p.split())
        if wc >= target_words:
            out.append({"text": "\n\n".join(buf)}); buf, wc = [], 0
    if buf:
        out.append({"text": "\n\n".join(buf)})
    return out


def all_passages(extracted_dir):
    out = []
    for path in sorted(glob.glob(os.path.join(extracted_dir, "*.txt"))):
        book = os.path.splitext(os.path.basename(path))[0]
        for c in passages(open(path, encoding="utf-8").read()):
            out.append({**c, "book": book})
    return out
