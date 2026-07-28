import re
import numpy as np

# Kompakte deutsche Stoppwortliste (erweiterbar).
STOP = set("""aber alle allem allen aller alles als also am an ander andere anderem anderen
anderer anderes auch auf aus bei beim bin bis bist da damit dann das dass dazu dein deine dem den
denn der des dessen deshalb die dies diese diesem diesen dieser dieses doch dort du durch ein eine
einem einen einer eines einige einigen einiger er es etwas euer eure für gegen gewesen hab habe
haben hat hatte hatten hier hin hinter ich ihm ihn ihnen ihr ihre ihrem ihren ihrer im in indem ins
ist ja jede jedem jeden jeder jedes jene jener jetzt kann kein keine können könnte machen man mehr
mein meine mit muss musste nach nicht nichts noch nun nur ob oder ohne schon sehr sein seine seinem
seinen seiner sich sie sind so solche solchem soll sollte sondern sonst über um und uns unser unsere
unter vom von vor war waren was weg weil weiter welche welchem welchen welcher wenn werde werden wie
wieder will wir wird wirst wo wollen wollte würde würden zu zum zur zwar zwischen mal ganz schon halt
eben also ok okay ja nein""".split())

_WORD = re.compile(r"[a-zäöüß]+", re.IGNORECASE)


def tokenize(text):
    text = re.sub(r"\(\d{1,2}:\d{2}(:\d{2})?\)", " ", text)   # (mm:ss) / (h:mm:ss)
    toks = [w.lower() for w in _WORD.findall(text)]
    return [w for w in toks if len(w) >= 3 and w not in STOP]


def tfidf_matrix(docs):
    tokenized = [tokenize(d) for d in docs]
    vocab = sorted({t for doc in tokenized for t in doc})
    vindex = {w: i for i, w in enumerate(vocab)}
    n, v = len(docs), len(vocab)
    counts = np.zeros((n, v))
    for i, doc in enumerate(tokenized):
        for t in doc:
            counts[i, vindex[t]] += 1.0
    # Relative Häufigkeit (Längen-Normalisierung): ein Wort wird nach Anteil an der
    # Dokumentlänge gewichtet, nicht nach absoluter Zahl — 2×/500 Wörter wiegt mehr
    # als 3×/5000 Wörter. Leere Dokumente bleiben Null.
    doc_len = counts.sum(axis=1, keepdims=True)
    doc_len[doc_len == 0] = 1.0
    tf = counts / doc_len
    df = (counts > 0).sum(axis=0)
    idf = np.log((1.0 + n) / (1.0 + df)) + 1.0                           # geglättete IDF
    mat = tf * idf
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return mat / norms


def cosine_dissim(mat):
    sim = mat @ mat.T
    np.clip(sim, -1.0, 1.0, out=sim)
    d = 1.0 - sim
    np.fill_diagonal(d, 0.0)
    return (d + d.T) / 2.0
