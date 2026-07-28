# Erleben-Karte v2 — Kapitel-Cluster mit NMDS-Layout — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die `/erleben`-Wissenskarte (Varianten Konstellation + Hybrid) auf die Kapitelstruktur des Quelldokuments umstellen: Knoten = Unterkapitel, vier Cluster = Kapitel 1–4, Knotenpositionen innerhalb eines Clusters per NMDS aus TF-IDF-Ähnlichkeit, cluster-übergreifende Kanten aus Ähnlichkeit + Kuratierung.

**Architecture:** Ein **offline** Python-Skript (`scripts/nmds-layout/`, nur `numpy`) berechnet aus den Transkripten einmalig `layout.json` (Cluster + x/y je Knoten + Kanten-Vorschläge). Ein Writer bäckt Cluster/x/y/related ins Frontmatter der Astro-Content-Dateien. Der Astro-Build bleibt statisch und rechnet nichts zur Laufzeit. `buildGraph()` liefert das Datenmodell unverändert an beide Zielvarianten; nur `GraphKonstellation.astro` bekommt Cluster-Hintergründe.

**Tech Stack:** Python 3 + numpy 2.x (offline Pipeline, keine sklearn-Abhängigkeit), Astro 5 Content Collections + Zod, vitest, TypeScript.

## Global Constraints

- **Urheberrecht:** Transkripte/Korpus bleiben gitignored (`scripts/nmds-layout/source|corpus|cache/`). Committet werden NUR abgeleitete Koordinaten/Kanten und eigene Zusammenfassungen — nie Transkripttext.
- **Keine neuen Runtime-Dependencies** im Astro-Projekt. NMDS ist ein Offline-Tool; `numpy` ist bereits vorhanden (2.4.5).
- **Determinismus:** Die Pipeline nutzt feste Seeds (`numpy.random.default_rng(42)`); `Date.now`/`Math.random` sind im Build tabu (bestehende Projektregel).
- **Farben nur aus bestehenden Tokens** (`homepage.css`): keine neuen Hexwerte. Cluster-Farbe nie alleiniger Bedeutungsträger — immer mit Text-Label.
- **Sprache Deutsch**, `lang="de"`; Labels/Titel in Amatic SC, sonst Avenir (bestehende Rollen).
- **Cluster-IDs:** `k1`=Grundlagen(`--ink`), `k2`=Herausforderungen(`--marker`), `k3`=Handwerk(`--ink-2`), `k4`=Praxisfälle(`--sun-deep`).
- **Knoten-Manifest (50, verbindlich)** — Slug → Doc-Überschrift(en) → Cluster (aus §3 des Specs):

  K1: erleben-erzeugen←1.9, hirnforschung←1.10, grundlagenmodell←1.11, netzwerk-modell←1.12+1.13, trance-transparenz←1.14, selbsterfahrung←1.15, probleme-basteln←1.16, potenzialhypothese←1.17, hypnosystemischer-ansatz←1.7, angst←1.8, sag-mal-gunther←1.3(„Sag mal, Gunther"), werdegang-wurzeln←1.3(„Werdegang & Wurzeln"), hypnosyst-denken←1.4, rollenverstaendnis←1.5, haltung←1.6
  K2: ursachen←2.1, symptomverstaendnis←2.2, neutralitaet←2.3, abgrenzung←2.4, diagnosen←2.5, burnout←2.6, entscheidungen←2.7, restriktionen←2.8, versoehnung←2.9, loesung-aller-probleme←2.10
  K3: beratungssystem←3.1.2, zuweisungsdynamik←3.1.3, auftragsklaerung←3.1.4, unterschiede←3.1.5, utilisation←3.1.6, steuerposition←3.1.7, interventionen←3.1.8, utilisation-problemsituationen←3.1.9, utilisation-ambivalenzen←3.1.10, utilisation-rueckfaelle←3.1.11, abschluss-transfer←3.1.12, fallanalyse-ungewisses←3.2, selbstfuersorge←3.3.2, eigene-wahrgebung←3.3.3, zugang-kompetenzen←3.3.4, imagination-steuerposition←3.3.5, innere-weisheit←3.3.6
  K4 (Text = jeweiliger „Überblick"): depression←4.2.4, trauer-schuld←4.3.3, schmerzen←4.4.4, panik←4.5.4, paarkonflikt←4.6.3, trauma←4.7.4, sucht←4.8.4, essverhalten←4.9.2 (kein Überblick vorhanden → „Kommentierung")

---

## File Structure

- `scripts/nmds-layout/manifest.py` — die 50 Knoten (slug, cluster, heading-keys, title). Single source of truth für die Pipeline.
- `scripts/nmds-layout/extract_corpus.py` — schneidet Knoten-Texte aus `source/doc.txt`.
- `scripts/nmds-layout/tfidf.py` — Tokenisierung + TF-IDF + Cluster-Dissimilaritätsmatrizen.
- `scripts/nmds-layout/nmds.py` — PAV (isotone Regression) + SMACOF-NMDS.
- `scripts/nmds-layout/build_layout.py` — Orchestrierung: Placement auf 100×100 + Kanten-Vorschläge → `out/layout.json`.
- `scripts/nmds-layout/write_frontmatter.py` — bäckt cluster/x/y/related in die `themen/*.md`, legt neue Stubs an.
- `scripts/nmds-layout/tests/` — pytest-freie, mit `python -m` lauffähige Assertions (stdlib `assert`), plus ein Runner.
- `scripts/nmds-layout/out/layout.json`, `edges.suggested.json`, `edges.curated.json` — committete Artefakte.
- `site/src/content.config.ts` — CLUSTERS-Enum k1..k4.
- `site/src/lib/graph.ts` — `Cluster`-Typ + `CLUSTER_META`.
- `site/src/lib/graph.test.ts` — Fixtures/Erwartungen auf k1..k4.
- `site/src/content/themen/*.md` — 30 remap + 20 neu.
- `site/src/components/graph/GraphKonstellation.astro` — Cluster-Hulls + Labels.

---

## Task 1: Manifest + Korpus-Extraktor

**Files:**
- Create: `scripts/nmds-layout/manifest.py`
- Create: `scripts/nmds-layout/extract_corpus.py`
- Create: `scripts/nmds-layout/tests/test_corpus.py`
- Uses: `scripts/nmds-layout/source/doc.txt` (bereits lokal abgelegt, gitignored)

**Interfaces:**
- Produces: `manifest.NODES: list[Node]` mit `Node = {"slug": str, "cluster": str, "headings": list[str], "title": str}` (headings = Nummern wie `"1.9"`, `"1.12"`; für netzwerk-modell zwei Einträge). `extract_corpus.build_corpus(doc_path) -> dict[slug, str]`.

- [ ] **Step 1: Write the failing test**

```python
# scripts/nmds-layout/tests/test_corpus.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from manifest import NODES
from extract_corpus import build_corpus

DOC = os.path.join(os.path.dirname(__file__), '..', 'source', 'doc.txt')

def test_manifest_shape():
    assert len(NODES) == 50, f"expected 50 nodes, got {len(NODES)}"
    clusters = {}
    for nd in NODES:
        clusters.setdefault(nd["cluster"], 0)
        clusters[nd["cluster"]] += 1
    assert clusters == {"k1": 15, "k2": 10, "k3": 17, "k4": 8}, clusters
    slugs = [nd["slug"] for nd in NODES]
    assert len(set(slugs)) == 50, "slugs not unique"

def test_corpus_covers_every_node_with_text():
    corpus = build_corpus(DOC)
    assert set(corpus.keys()) == {nd["slug"] for nd in NODES}
    for slug, text in corpus.items():
        assert len(text.split()) >= 40, f"{slug} too short: {len(text.split())} words"

if __name__ == "__main__":
    test_manifest_shape(); test_corpus_covers_every_node_with_text()
    print("OK test_corpus")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts/nmds-layout && python3 tests/test_corpus.py`
Expected: FAIL (`ModuleNotFoundError: No module named 'manifest'`)

- [ ] **Step 3: Write the manifest**

```python
# scripts/nmds-layout/manifest.py
# Slug -> (cluster, heading-keys, title). heading-keys sind die Doc-Nummern.
# netzwerk-modell fasst 1.12 + 1.13 zusammen. K4 nutzt die "Überblick"-Nummer.
_RAW = [
    # K1 Grundlagen
    ("sag-mal-gunther", "k1", ["1.3s"], "Sag mal, Gunther …"),
    ("werdegang-wurzeln", "k1", ["1.3w"], "Werdegang & Wurzeln"),
    ("hypnosyst-denken", "k1", ["1.4"], "Hypnosystemisches Denken"),
    ("rollenverstaendnis", "k1", ["1.5"], "Hypnosystemisches Rollenverständnis"),
    ("haltung", "k1", ["1.6"], "Hypnosystemische Haltung"),
    ("hypnosystemischer-ansatz", "k1", ["1.7"], "Ansatz auf den Punkt"),
    ("angst", "k1", ["1.8"], "Praxisbeispiel Angst"),
    ("erleben-erzeugen", "k1", ["1.9"], "Wie erzeugen wir unser Erleben?"),
    ("hirnforschung", "k1", ["1.10"], "Erkenntnisse der Hirnforschung"),
    ("grundlagenmodell", "k1", ["1.11"], "Elementares Grundlagenmodell"),
    ("netzwerk-modell", "k1", ["1.12", "1.13"], "Netzwerk-Modell"),
    ("trance-transparenz", "k1", ["1.14"], "Trance & Transparenz"),
    ("selbsterfahrung", "k1", ["1.15"], "Selbsterfahrung"),
    ("probleme-basteln", "k1", ["1.16"], "Bastelanleitung für Probleme"),
    ("potenzialhypothese", "k1", ["1.17"], "Potenzialhypothese"),
    # K2 Herausforderungen
    ("ursachen", "k2", ["2.1"], "Bedeutung von Ursachen"),
    ("symptomverstaendnis", "k2", ["2.2"], "Symptomverständnis"),
    ("neutralitaet", "k2", ["2.3"], "Neutralität"),
    ("abgrenzung", "k2", ["2.4"], "Abgrenzungsfähigkeit"),
    ("diagnosen", "k2", ["2.5"], "Diagnosen"),
    ("burnout", "k2", ["2.6"], "Burnout"),
    ("entscheidungen", "k2", ["2.7"], "Entscheidungssituationen"),
    ("restriktionen", "k2", ["2.8"], "Umgang mit Restriktionen"),
    ("versoehnung", "k2", ["2.9"], "Das Konzept der Versöhnung"),
    ("loesung-aller-probleme", "k2", ["2.10"], "Die Lösung aller Probleme"),
    # K3 Handwerk
    ("beratungssystem", "k3", ["3.1.2"], "Beratungssystem & Utilisationsansatz"),
    ("zuweisungsdynamik", "k3", ["3.1.3"], "Klärung der Zuweisungs-Dynamik"),
    ("auftragsklaerung", "k3", ["3.1.4"], "Auftragsklärung"),
    ("unterschiede", "k3", ["3.1.5"], "Fokus auf Unterschiede"),
    ("utilisation", "k3", ["3.1.6"], "Utilisation von Unterschieden"),
    ("steuerposition", "k3", ["3.1.7"], "Aufbau einer Steuerposition"),
    ("interventionen", "k3", ["3.1.8"], "Weitere Interventionen"),
    ("utilisation-problemsituationen", "k3", ["3.1.9"], "Utilisation von Problemsituationen"),
    ("utilisation-ambivalenzen", "k3", ["3.1.10"], "Utilisation von Ambivalenzen"),
    ("utilisation-rueckfaelle", "k3", ["3.1.11"], "Utilisation von Rückfällen"),
    ("abschluss-transfer", "k3", ["3.1.12"], "Abschluss & Transfer"),
    ("fallanalyse-ungewisses", "k3", ["3.2"], "Fallanalyse: Umgang mit dem Ungewissen"),
    ("selbstfuersorge", "k3", ["3.3.2"], "Selbstfürsorge"),
    ("eigene-wahrgebung", "k3", ["3.3.3"], "Utilisation der eigenen „Wahrgebung“"),
    ("zugang-kompetenzen", "k3", ["3.3.4"], "Optimaler Zugang zu Kompetenzen"),
    ("imagination-steuerposition", "k3", ["3.3.5"], "Imagination: Steuerposition"),
    ("innere-weisheit", "k3", ["3.3.6"], "Imagination: Innere Weisheit"),
    # K4 Praxisfälle (Text = Überblick)
    ("depression", "k4", ["4.2.4"], "Depressionen"),
    ("trauer-schuld", "k4", ["4.3.3"], "Trauer & Schuld"),
    ("schmerzen", "k4", ["4.4.4"], "Chronische Schmerzen"),
    ("panik", "k4", ["4.5.4"], "Panikattacken"),
    ("paarkonflikt", "k4", ["4.6.3"], "Paarkonflikt"),
    ("trauma", "k4", ["4.7.4"], "Trauma"),
    ("sucht", "k4", ["4.8.4"], "Alkohol- und Nikotinsucht"),
    ("essverhalten", "k4", ["4.9.2"], "Ess- und Bewegungsgewohnheiten"),
]
NODES = [{"slug": s, "cluster": c, "headings": h, "title": t} for (s, c, h, t) in _RAW]
BY_SLUG = {n["slug"]: n for n in NODES}
```

- [ ] **Step 4: Write the corpus extractor**

Doc-Headings sind Markdown: `## N Titel` bzw. `### N Titel`. Sonderfälle: die beiden 1.3-Abschnitte werden über den Titel unterschieden (`1.3s`→enthält „Sag mal", `1.3w`→enthält „Werdegang"). Jeder Knoten-Text reicht von seiner Überschrift bis zur nächsten Überschrift gleicher/höherer Ebene.

```python
# scripts/nmds-layout/extract_corpus.py
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
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd scripts/nmds-layout && python3 tests/test_corpus.py`
Expected: `OK test_corpus`
(Falls ein Knoten <40 Wörter liefert: heading-key gegen `source/doc.txt` prüfen und `manifest.py`/`_key_for` korrigieren.)

- [ ] **Step 6: Commit**

```bash
git add scripts/nmds-layout/manifest.py scripts/nmds-layout/extract_corpus.py scripts/nmds-layout/tests/test_corpus.py
git commit -m "NMDS-Pipeline: Manifest (50 Knoten) + Korpus-Extraktor"
```

---

## Task 2: TF-IDF + Cluster-Dissimilaritätsmatrizen

**Files:**
- Create: `scripts/nmds-layout/tfidf.py`
- Create: `scripts/nmds-layout/tests/test_tfidf.py`

**Interfaces:**
- Consumes: `build_corpus` (Task 1).
- Produces: `tfidf.tokenize(text) -> list[str]`; `tfidf.tfidf_matrix(docs: list[str]) -> np.ndarray (n×v, L2-normiert)`; `tfidf.cosine_dissim(mat) -> np.ndarray (n×n, 1−cos, diag=0)`.

- [ ] **Step 1: Write the failing test**

```python
# scripts/nmds-layout/tests/test_tfidf.py
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tfidf import tokenize, tfidf_matrix, cosine_dissim

def test_tokenize_strips_timestamps_and_stopwords():
    toks = tokenize("Das Erleben (19:37) ist und der die das Netzwerk.")
    assert "erleben" in toks and "netzwerk" in toks
    assert "und" not in toks and "der" not in toks
    assert not any(":" in t for t in toks)

def test_dissim_is_symmetric_zero_diag_and_deterministic():
    docs = ["erleben netzwerk trance", "erleben netzwerk fokus", "diagnose symptom ursache"]
    m1 = cosine_dissim(tfidf_matrix(docs))
    m2 = cosine_dissim(tfidf_matrix(docs))
    assert np.allclose(m1, m1.T)
    assert np.allclose(np.diag(m1), 0.0)
    assert np.array_equal(m1, m2)                    # deterministisch
    assert m1[0, 1] < m1[0, 2]                       # 0 & 1 ähnlicher als 0 & 2

if __name__ == "__main__":
    test_tokenize_strips_timestamps_and_stopwords()
    test_dissim_is_symmetric_zero_diag_and_deterministic()
    print("OK test_tfidf")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts/nmds-layout && python3 tests/test_tfidf.py`
Expected: FAIL (`No module named 'tfidf'`)

- [ ] **Step 3: Write the implementation**

```python
# scripts/nmds-layout/tfidf.py
import re, math
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
    tf = np.zeros((n, v))
    for i, doc in enumerate(tokenized):
        for t in doc:
            tf[i, vindex[t]] += 1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        tf = np.where(tf > 0, 1.0 + np.log(tf, where=tf > 0), 0.0)  # sublineare TF
    df = (tf > 0).sum(axis=0)
    idf = np.log((1.0 + n) / (1.0 + df)) + 1.0                      # geglättete IDF
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd scripts/nmds-layout && python3 tests/test_tfidf.py`
Expected: `OK test_tfidf`

- [ ] **Step 5: Commit**

```bash
git add scripts/nmds-layout/tfidf.py scripts/nmds-layout/tests/test_tfidf.py
git commit -m "NMDS-Pipeline: TF-IDF + Kosinus-Dissimilarität"
```

---

## Task 3: NMDS (isotone Regression + SMACOF)

**Files:**
- Create: `scripts/nmds-layout/nmds.py`
- Create: `scripts/nmds-layout/tests/test_nmds.py`

**Interfaces:**
- Produces: `nmds.pav(y, w) -> np.ndarray` (monoton nicht-fallende Anpassung); `nmds.nmds(D, seed=42, restarts=8, iters=300) -> (Y: np.ndarray n×2, stress: float)`. Non-metrisch: passt Disparitäten an die **Rangordnung** von D an (Kruskal Stress-1).

- [ ] **Step 1: Write the failing test**

```python
# scripts/nmds-layout/tests/test_nmds.py
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from nmds import pav, nmds

def test_pav_is_monotone():
    out = pav(np.array([3.0, 1.0, 2.0, 4.0]), np.ones(4))
    assert np.all(np.diff(out) >= -1e-9), out

def test_nmds_deterministic_and_recovers_line():
    # 5 Punkte auf einer Linie -> Rangordnung der Distanzen in 2D erhalten
    true = np.array([[0,0],[1,0],[2,0],[3,0],[4,0]], float)
    D = np.sqrt(((true[:,None,:]-true[None,:,:])**2).sum(-1))
    Y1, s1 = nmds(D, seed=42)
    Y2, s2 = nmds(D, seed=42)
    assert np.allclose(Y1, Y2) and abs(s1 - s2) < 1e-12      # deterministisch
    assert s1 < 0.05                                          # niedriger Stress
    # Rangordnung: Nachbardistanzen < Randdistanz
    d01 = np.linalg.norm(Y1[0]-Y1[1]); d04 = np.linalg.norm(Y1[0]-Y1[4])
    assert d01 < d04

if __name__ == "__main__":
    test_pav_is_monotone(); test_nmds_deterministic_and_recovers_line()
    print("OK test_nmds")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts/nmds-layout && python3 tests/test_nmds.py`
Expected: FAIL (`No module named 'nmds'`)

- [ ] **Step 3: Write the implementation**

```python
# scripts/nmds-layout/nmds.py
import numpy as np

def pav(y, w):
    """Pool-Adjacent-Violators: gewichtete isotone (nicht-fallende) Regression."""
    y = y.astype(float).copy(); w = w.astype(float).copy()
    n = len(y)
    val = y.copy(); wt = w.copy(); idx = list(range(n)); size = [1]*n
    # Blocks als Stack
    lvl_val = []; lvl_w = []; lvl_n = []
    for i in range(n):
        cv, cw, cn = y[i], w[i], 1
        while lvl_val and lvl_val[-1] > cv:
            pv, pw, pn = lvl_val.pop(), lvl_w.pop(), lvl_n.pop()
            cv = (pv*pw + cv*cw) / (pw + cw)
            cw = pw + cw; cn = pn + cn
        lvl_val.append(cv); lvl_w.append(cw); lvl_n.append(cn)
    out = np.empty(n); k = 0
    for v, cnt in zip(lvl_val, lvl_n):
        out[k:k+cnt] = v; k += cnt
    return out

def _stress(D, Y, disp):
    d = np.linalg.norm(Y[:,None,:]-Y[None,:,:], axis=-1)
    iu = np.triu_indices(len(D), 1)
    num = np.sum((disp[iu]-d[iu])**2)
    den = np.sum(d[iu]**2)
    return np.sqrt(num/den) if den > 0 else 0.0

def _smacof_once(D, Y, iters):
    n = len(D)
    iu = np.triu_indices(n, 1)
    order = np.argsort(D[iu], kind="mergesort")   # stabile Rangordnung
    prev = None
    for _ in range(iters):
        d = np.linalg.norm(Y[:,None,:]-Y[None,:,:], axis=-1)
        # Disparitäten: isotone Regression der Distanzen entlang der D-Rangordnung
        dvec = d[iu][order]
        disp_sorted = pav(dvec, np.ones(len(dvec)))
        disp = np.zeros((n, n))
        tmp = np.empty(len(order)); tmp[order] = disp_sorted
        disp[iu] = tmp; disp = disp + disp.T
        # Guttman-Transform (SMACOF) mit disp als Ziel-Distanzen
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(d > 1e-12, disp / d, 0.0)
        B = -ratio; np.fill_diagonal(B, 0.0)
        np.fill_diagonal(B, -B.sum(axis=1))
        Y = (B @ Y) / n
        s = _stress(D, Y, disp)
        if prev is not None and abs(prev - s) < 1e-9:
            break
        prev = s
    return Y, _stress(D, Y, disp)

def nmds(D, seed=42, restarts=8, iters=300):
    D = np.asarray(D, float)
    n = len(D)
    if n == 1:
        return np.zeros((1, 2)), 0.0
    rng = np.random.default_rng(seed)
    best_Y, best_s = None, np.inf
    # Init 0: klassisches MDS (Torgerson) als deterministischer Startpunkt
    inits = [_classical_mds(D)]
    for _ in range(restarts - 1):
        inits.append(rng.standard_normal((n, 2)))
    for Y0 in inits:
        Y, s = _smacof_once(D, Y0.copy(), iters)
        if s < best_s:
            best_s, best_Y = s, Y
    return best_Y, best_s

def _classical_mds(D):
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D**2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:2]
    L = np.clip(w[idx], 0, None)
    return V[:, idx] * np.sqrt(L)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd scripts/nmds-layout && python3 tests/test_nmds.py`
Expected: `OK test_nmds`

- [ ] **Step 5: Commit**

```bash
git add scripts/nmds-layout/nmds.py scripts/nmds-layout/tests/test_nmds.py
git commit -m "NMDS-Pipeline: isotone Regression (PAV) + SMACOF-NMDS"
```

---

## Task 4: Placement auf die Bühne + Kanten-Vorschläge → layout.json

**Files:**
- Create: `scripts/nmds-layout/build_layout.py`
- Create: `scripts/nmds-layout/tests/test_layout.py`
- Produces (committed): `scripts/nmds-layout/out/layout.json`, `scripts/nmds-layout/out/edges.suggested.json`

**Interfaces:**
- Consumes: `build_corpus`, `tfidf_matrix`, `cosine_dissim`, `nmds`, `manifest.NODES`.
- Produces: `build_layout.build(doc_path) -> dict` mit `{"nodes": {slug: {"cluster","x","y"}}, "edges_suggested": [{"a","b","sim"}]}`. Vier Cluster-Regionen auf 100×100 (2×2), Puffer dazwischen; jede Cluster-Wolke isotrop skaliert/zentriert in ihre Region. Kanten-Vorschläge = Top cross-cluster-Kosinus-Paare über Schwelle.

**Region-Layout (verbindlich):** Canvas 100×100, Regionen mit 6 % Innen-Padding:
`k1`=(links oben) x∈[6,46] y∈[8,46] · `k2`=(rechts oben) x∈[54,94] y∈[8,46] · `k3`=(links unten) x∈[6,46] y∈[54,92] · `k4`=(rechts unten) x∈[54,94] y∈[54,92].

- [ ] **Step 1: Write the failing test**

```python
# scripts/nmds-layout/tests/test_layout.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build_layout import build, REGIONS

DOC = os.path.join(os.path.dirname(__file__), '..', 'source', 'doc.txt')

def test_layout_bounds_and_edges():
    L = build(DOC)
    assert len(L["nodes"]) == 50
    for slug, p in L["nodes"].items():
        rx0, rx1, ry0, ry1 = REGIONS[p["cluster"]]
        assert rx0 - 0.01 <= p["x"] <= rx1 + 0.01, (slug, p)
        assert ry0 - 0.01 <= p["y"] <= ry1 + 0.01, (slug, p)
    # Kanten-Vorschläge: cross-cluster, symmetriefrei (a<b), sim absteigend
    clby = {s: p["cluster"] for s, p in L["nodes"].items()}
    for e in L["edges_suggested"]:
        assert clby[e["a"]] != clby[e["b"]], e
        assert e["a"] < e["b"]
    sims = [e["sim"] for e in L["edges_suggested"]]
    assert sims == sorted(sims, reverse=True)
    assert len(L["edges_suggested"]) >= 8

def test_build_is_deterministic():
    a = build(DOC); b = build(DOC)
    assert a == b

if __name__ == "__main__":
    test_layout_bounds_and_edges(); test_build_is_deterministic()
    print("OK test_layout")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts/nmds-layout && python3 tests/test_layout.py`
Expected: FAIL (`No module named 'build_layout'`)

- [ ] **Step 3: Write the implementation**

```python
# scripts/nmds-layout/build_layout.py
import json, os
import numpy as np
from manifest import NODES
from extract_corpus import build_corpus
from tfidf import tfidf_matrix, cosine_dissim
from nmds import nmds

REGIONS = {  # x0, x1, y0, y1
    "k1": (6, 46, 8, 46), "k2": (54, 94, 8, 46),
    "k3": (6, 46, 54, 92), "k4": (54, 94, 54, 92),
}
CROSS_EDGE_MIN_SIM = 0.10   # Schwelle für Kanten-Vorschläge
CROSS_EDGE_TOPK = 40        # Deckel auf die Vorschlagsliste

def _fit_region(Y, region):
    """Y (n×2) isotrop in die Region skalieren, zentriert, Aspect erhalten."""
    x0, x1, y0, y1 = region
    if len(Y) == 1:
        return np.array([[(x0+x1)/2, (y0+y1)/2]])
    Y = Y - Y.mean(axis=0)
    span = np.max(np.abs(Y)) * 2 or 1.0
    w, h = (x1 - x0), (y1 - y0)
    scale = min(w, h) / span * 0.92
    Y = Y * scale
    return Y + np.array([(x0 + x1) / 2, (y0 + y1) / 2])

def build(doc_path):
    corpus = build_corpus(doc_path)
    slugs = [n["slug"] for n in NODES]
    docs = [corpus[s] for s in slugs]
    mat = tfidf_matrix(docs)                 # globale TF-IDF (ein Vokabular)
    sidx = {s: i for i, s in enumerate(slugs)}
    nodes = {}
    for cl in ("k1", "k2", "k3", "k4"):
        members = [n["slug"] for n in NODES if n["cluster"] == cl]
        idx = [sidx[s] for s in members]
        sub = mat[idx]
        D = cosine_dissim(sub)
        Y, _ = nmds(D, seed=42)
        Y = _fit_region(Y, REGIONS[cl])
        for s, (x, y) in zip(members, Y):
            nodes[s] = {"cluster": cl, "x": round(float(x), 2), "y": round(float(y), 2)}
    # Cross-Cluster-Kanten-Vorschläge
    sim = mat @ mat.T
    edges = []
    for i in range(len(slugs)):
        for j in range(i + 1, len(slugs)):
            if nodes[slugs[i]]["cluster"] == nodes[slugs[j]]["cluster"]:
                continue
            sc = float(sim[i, j])
            if sc >= CROSS_EDGE_MIN_SIM:
                a, b = sorted((slugs[i], slugs[j]))
                edges.append({"a": a, "b": b, "sim": round(sc, 4)})
    edges.sort(key=lambda e: e["sim"], reverse=True)
    edges = edges[:CROSS_EDGE_TOPK]
    return {"nodes": nodes, "edges_suggested": edges}

if __name__ == "__main__":
    here = os.path.dirname(__file__)
    doc = os.path.join(here, "source", "doc.txt")
    L = build(doc)
    os.makedirs(os.path.join(here, "out"), exist_ok=True)
    json.dump(L["nodes"], open(os.path.join(here, "out", "layout.json"), "w"),
              ensure_ascii=False, indent=2, sort_keys=True)
    json.dump(L["edges_suggested"], open(os.path.join(here, "out", "edges.suggested.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"layout.json: {len(L['nodes'])} Knoten; {len(L['edges_suggested'])} Kanten-Vorschläge")
```

- [ ] **Step 4: Run test + generate artifacts**

Run: `cd scripts/nmds-layout && python3 tests/test_layout.py && python3 build_layout.py`
Expected: `OK test_layout` und `layout.json: 50 Knoten; N Kanten-Vorschläge`

- [ ] **Step 5: Commit**

```bash
git add scripts/nmds-layout/build_layout.py scripts/nmds-layout/tests/test_layout.py scripts/nmds-layout/out/layout.json scripts/nmds-layout/out/edges.suggested.json
git commit -m "NMDS-Pipeline: Cluster-Placement + Kanten-Vorschläge (layout.json)"
```

---

## Task 5: Kanten kuratieren

**Files:**
- Create: `scripts/nmds-layout/out/edges.curated.json`

**Interfaces:**
- Consumes: `out/edges.suggested.json` (Task 4) + bestehende `related`-Kanten aus `themen/*.md`.
- Produces: `edges.curated.json` = `[["a","b"], ...]` (finale cluster-übergreifende Kantenliste, fachlich geprüft).

- [ ] **Step 1: Vorschläge + Bestand sichten**

Run: `cat scripts/nmds-layout/out/edges.suggested.json` und
`grep -rl "related:" site/src/content/themen/ | head` — vorhandene `related`-Listen der 30 Altdateien überfliegen (die sind bereits fachlich gesetzt).

- [ ] **Step 2: Kuratierte Liste schreiben**

Regeln für die Auswahl (dokumentiert, damit reproduzierbar nachvollziehbar):
1. Jeden Vorschlag mit `sim ≥ 0.10` übernehmen, der fachlich plausibel ist (Konzept-Bezug, nicht nur Vokabel-Zufall).
2. Fachlich offensichtliche cross-cluster-Brücken ergänzen, auch wenn knapp unter Schwelle — mindestens: `angst`↔`panik`, `probleme-basteln`↔`symptomverstaendnis`, `potenzialhypothese`↔`innere-weisheit`, `burnout`↔`selbstfuersorge`, `netzwerk-modell`↔`ursachen`, `depression`↔`symptomverstaendnis`, `trauma`↔`neutralitaet`.
3. Reine Vokabel-Artefakte streichen (z. B. wenn zwei Fälle nur „Sitzung/Klient" teilen).
4. Nur cluster-übergreifende Kanten hier (cluster-interne Nähe steckt schon in x/y).

Schreibe die finale Liste als JSON-Array von `[a, b]`-Paaren (a<b) nach
`scripts/nmds-layout/out/edges.curated.json`. Beispiel-Gerüst:

```json
[
  ["angst", "panik"],
  ["burnout", "selbstfuersorge"],
  ["depression", "symptomverstaendnis"],
  ["netzwerk-modell", "ursachen"],
  ["potenzialhypothese", "innere-weisheit"],
  ["probleme-basteln", "symptomverstaendnis"],
  ["trauma", "neutralitaet"]
]
```

- [ ] **Step 3: Validieren**

Run:
```bash
cd scripts/nmds-layout && python3 -c "
import json
from manifest import BY_SLUG
E=json.load(open('out/edges.curated.json'))
for a,b in E:
    assert a in BY_SLUG and b in BY_SLUG, (a,b)
    assert a<b, (a,b)
    assert BY_SLUG[a]['cluster']!=BY_SLUG[b]['cluster'], (a,b)
assert len({tuple(e) for e in E})==len(E), 'Duplikate'
print('edges.curated.json OK:', len(E), 'Kanten')
"
```
Expected: `edges.curated.json OK: N Kanten`

- [ ] **Step 4: Commit**

```bash
git add scripts/nmds-layout/out/edges.curated.json
git commit -m "NMDS-Pipeline: kuratierte cluster-übergreifende Kanten"
```

---

## Task 6: Datenmodell graph.ts + Unit-Tests auf k1..k4

**Files:**
- Modify: `site/src/lib/graph.ts:1` (Cluster-Typ) und `:12-18` (CLUSTER_META)
- Modify: `site/src/lib/graph.test.ts` (Fixtures + Cluster-Erwartung)

**Interfaces:**
- Produces: `Cluster = 'k1'|'k2'|'k3'|'k4'`; `CLUSTER_META` mit vier Einträgen (id/label/colorVar). `assembleGraph`/`buildGraph`-Signaturen unverändert.

- [ ] **Step 1: Test auf neue Cluster umstellen (failing)**

Ersetze in `site/src/lib/graph.test.ts` die Fixture-Cluster und die Cluster-Erwartung:

```ts
const n = (slug: string, related: string[] = []): RawNode => ({
  slug, title: slug, cluster: 'k1', summary: 's',
  x: 10, y: 20, status: 'stub', related,
});
```
und den dritten Test:
```ts
  it('liefert alle vier Kapitel-Cluster-Metadaten', () => {
    const g = assembleGraph([n('a')]);
    expect(g.clusters.map((c) => c.id)).toEqual(['k1', 'k2', 'k3', 'k4']);
    expect(g.clusters[1]).toMatchObject({ id: 'k2', colorVar: '--marker' });
  });
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd site && npx vitest run src/lib/graph.test.ts`
Expected: FAIL (Typfehler `'k1'` nicht in `Cluster` / Cluster-Liste ≠ erwartet)

- [ ] **Step 3: graph.ts anpassen**

`site/src/lib/graph.ts` Zeile 1 und 12–18:
```ts
export type Cluster = 'k1' | 'k2' | 'k3' | 'k4';
```
```ts
export const CLUSTER_META: ClusterMeta[] = [
  { id: 'k1', label: 'Grundlagen', colorVar: '--ink' },
  { id: 'k2', label: 'Herausforderungen', colorVar: '--marker' },
  { id: 'k3', label: 'Handwerk', colorVar: '--ink-2' },
  { id: 'k4', label: 'Praxisfälle', colorVar: '--sun-deep' },
];
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd site && npx vitest run src/lib/graph.test.ts`
Expected: PASS (4 Tests grün)

- [ ] **Step 5: Commit**

```bash
git add site/src/lib/graph.ts site/src/lib/graph.test.ts
git commit -m "Erleben v2: Datenmodell auf Kapitel-Cluster k1–k4"
```

---

## Task 7: Frontmatter-Writer — 30 remap + 20 neue Stubs, Build grün

**Files:**
- Create: `scripts/nmds-layout/write_frontmatter.py`
- Modify: `site/src/content.config.ts:4` (CLUSTERS)
- Modify/Create: `site/src/content/themen/*.md` (alle 50)

**Interfaces:**
- Consumes: `out/layout.json`, `out/edges.curated.json`, `manifest.NODES`, bestehende `themen/*.md`.
- Effekt: Jede Knotendatei erhält `cluster`, `x`, `y` aus layout.json und die aus `edges.curated.json` abgeleiteten cross-cluster-`related`-Einträge (mit bestehenden intra-cluster-`related` gemergt). Neue Knoten werden als Stub angelegt.

**Writer-Regeln:**
- Bestehende Datei: nur Frontmatter-Felder `cluster`/`x`/`y` setzen; `related` = Union(bestehende related, kuratierte Kanten mit diesem Slug); `title`/`summary`/`status`/Body **unverändert**.
- Neue Datei: Stub mit `title` (aus Manifest), `cluster`, `x`, `y`, `status: stub`, `summary` (Platzhalter, im nächsten Schritt ersetzt), `related` (kuratierte Kanten), Body „Inhalt folgt.".
- `related` darf keine baumelnden Slugs enthalten (alle 50 existieren nach dem Lauf).

- [ ] **Step 1: Writer schreiben**

```python
# scripts/nmds-layout/write_frontmatter.py
import json, os, re
from manifest import NODES, BY_SLUG

HERE = os.path.dirname(__file__)
THEMEN = os.path.normpath(os.path.join(HERE, "..", "..", "site", "src", "content", "themen"))
layout = json.load(open(os.path.join(HERE, "out", "layout.json")))
curated = json.load(open(os.path.join(HERE, "out", "edges.curated.json")))

rel_from_edges = {}
for a, b in curated:
    rel_from_edges.setdefault(a, set()).add(b)
    rel_from_edges.setdefault(b, set()).add(a)

FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)

def parse_related(fm_text):
    m = re.search(r"^related:\s*\[(.*?)\]\s*$", fm_text, re.M)
    if not m or not m.group(1).strip():
        return []
    return [x.strip().strip('"').strip("'") for x in m.group(1).split(",") if x.strip()]

def parse_field(fm_text, key, default=""):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm_text, re.M)
    return m.group(1) if m else default

def render(slug, title, cluster, x, y, summary, related, status, body):
    rel = "[" + ", ".join(sorted(set(related))) + "]"
    fm = (f'---\ntitle: "{title}"\ncluster: {cluster}\n'
          f'summary: "{summary}"\nrelated: {rel}\n'
          f'x: {x}\ny: {y}\nstatus: {status}\n---\n')
    return fm + body

def main():
    for nd in NODES:
        slug = nd["slug"]; pos = layout[slug]
        path = os.path.join(THEMEN, slug + ".md")
        edge_rel = rel_from_edges.get(slug, set())
        if os.path.exists(path):
            raw = open(path, encoding="utf-8").read()
            m = FM.match(raw); fm_text, body = m.group(1), m.group(2)
            title = parse_field(fm_text, "title", nd["title"])
            summary = parse_field(fm_text, "summary", "")
            status = parse_field(fm_text, "status", "stub")
            related = sorted(set(parse_related(fm_text)) | edge_rel)
        else:
            title = nd["title"]; summary = f"{title} — Zusammenfassung folgt."
            status = "stub"; body = "\nInhalt folgt.\n"
            related = sorted(edge_rel)
        out = render(slug, title, pos["cluster"], pos["x"], pos["y"],
                     summary, related, status, body)
        open(path, "w", encoding="utf-8").write(out)
    print("Frontmatter geschrieben:", len(NODES), "Dateien")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: CLUSTERS-Enum umstellen**

`site/src/content.config.ts` Zeile 4:
```ts
export const CLUSTERS = ['k1', 'k2', 'k3', 'k4'] as const;
```

- [ ] **Step 3: Writer laufen lassen**

Run: `cd scripts/nmds-layout && python3 write_frontmatter.py`
Expected: `Frontmatter geschrieben: 50 Dateien`
Danach prüfen: `ls site/src/content/themen | wc -l` → `50`.

- [ ] **Step 4: Integritäts-Check (kein baumelnder related, alle in einem Cluster)**

Run:
```bash
cd site && npx vitest run src/lib/graph.test.ts && npm run build 2>&1 | tail -20
```
Expected: vitest grün; `npm run build` erzeugt `/erleben`, `/erleben/konstellation`, `/erleben/hybrid` und 50 `thema`-Seiten ohne Fehler. (Bei „Baumelnder related-Slug"-Fehler: `edges.curated.json` referenziert einen nicht existenten Slug → korrigieren, Writer erneut laufen lassen.)

- [ ] **Step 5: Commit**

```bash
git add scripts/nmds-layout/write_frontmatter.py site/src/content.config.ts site/src/content/themen
git commit -m "Erleben v2: Kapitel-Cluster + NMDS-Positionen ins Frontmatter (50 Knoten)"
```

---

## Task 8: GraphKonstellation — Cluster-Hulls + Labels (Klenico-Stil)

**Files:**
- Modify: `site/src/components/graph/GraphKonstellation.astro`

**Interfaces:**
- Consumes: `Graph` (nodes mit cluster/x/y), `CLUSTER_META`.
- Effekt: pro Cluster ein getönter Hintergrund-Bereich (Bounding-Box der Cluster-Knoten + Padding) in Cluster-Farbe (niedrige Deckkraft) mit Cluster-Titel (Amatic). Bestehende Knoten/Kanten/Gold-Hover unverändert.

- [ ] **Step 1: Cluster-Regionen im Frontmatter-Teil berechnen**

In `GraphKonstellation.astro` nach `const colorOf = …` einfügen:
```ts
const PAD = 3; // % Padding um die Cluster-Wolke
const regions = CLUSTER_META.map((c) => {
  const ns = graph.nodes.filter((n) => n.cluster === c.id);
  const xs = ns.map((n) => n.x), ys = ns.map((n) => n.y);
  const x0 = Math.max(0, Math.min(...xs) - PAD), x1 = Math.min(100, Math.max(...xs) + PAD);
  const y0 = Math.max(0, Math.min(...ys) - PAD), y1 = Math.min(100, Math.max(...ys) + PAD);
  return { ...c, x0, y0, w: x1 - x0, h: y1 - y0 };
}).filter((r) => r.w > 0 && r.h > 0);
```

- [ ] **Step 2: Regionen + Labels rendern**

Direkt nach dem öffnenden `<div class="konstellation" …>` (vor dem `<svg class="edges">`) einfügen:
```astro
  {regions.map((r) => (
    <div class="cluster-region" style={`left:${r.x0}%; top:${r.y0}%; width:${r.w}%; height:${r.h}%; --c: var(${r.colorVar})`}>
      <span class="cluster-label">{r.label}</span>
    </div>
  ))}
```

- [ ] **Step 3: Styles ergänzen**

Im `<style>`-Block ergänzen (nach `.konstellation { … }`):
```css
  .cluster-region {
    position: absolute; border-radius: 18px;
    background: color-mix(in srgb, var(--c) 9%, transparent);
    border: 1px solid color-mix(in srgb, var(--c) 18%, transparent);
    pointer-events: none; z-index: 0;
  }
  .cluster-label {
    position: absolute; top: 6px; left: 12px;
    font-family: var(--font-hand); font-weight: 700; font-size: 18px;
    color: color-mix(in srgb, var(--c) 70%, var(--ink)); opacity: .8;
  }
  .konstellation .edges, .konstellation .node { z-index: 1; }
```

- [ ] **Step 4: Build + Sichtprüfung**

Run: `cd site && npm run build 2>&1 | tail -5 && npx astro check 2>&1 | tail -5`
Expected: Build ok, `astro check` ohne Fehler. Vier getönte Cluster-Bereiche mit Titeln, Knoten/Kanten darüber.

- [ ] **Step 5: Commit**

```bash
git add site/src/components/graph/GraphKonstellation.astro
git commit -m "Erleben v2: Cluster-Hulls + Kapitel-Labels (Klenico-Stil)"
```

---

## Task 9: K4-Summaries + Gesamt-Verifikation

**Files:**
- Modify: `site/src/content/themen/{depression,trauer-schuld,schmerzen,panik,paarkonflikt,trauma,sucht,essverhalten}.md` (K4) und die neuen K1/K3-Stubs (Summaries)

**Interfaces:** keine (Content-Feinschliff + Abnahme).

- [ ] **Step 1: Summaries setzen**

Für die 8 K4-Fälle und die neuen K1/K3-Knoten je einen prägnanten deutschen Summary-Satz (aus dem „Überblick"/Abschnitt, in eigener Formulierung — keine Transkriptzitate) ins `summary`-Feld schreiben. Body bleibt „Inhalt folgt." (Stub). Beispiel `depression.md`:
```
summary: "Depression als eingefrorenes Erleben — hypnosystemisch als verlorener Zugang zu eigenen Kompetenzen und Ambivalenzen verstanden und bearbeitet."
```

- [ ] **Step 2: Determinismus der Pipeline bestätigen**

Run:
```bash
cd scripts/nmds-layout && python3 build_layout.py && git diff --stat out/layout.json
```
Expected: **keine** Änderung an `out/layout.json` (fester Seed → identisch).

- [ ] **Step 3: Volltest**

Run:
```bash
cd scripts/nmds-layout && for t in tests/test_*.py; do python3 "$t"; done
cd ../../site && npx vitest run && npm run build 2>&1 | tail -8 && npx astro check 2>&1 | tail -5
```
Expected: alle Pipeline-Tests `OK`, vitest grün, Build erzeugt alle Seiten, `astro check` fehlerfrei.

- [ ] **Step 4: Manuelle Abnahme (Checkliste)**

- [ ] `/erleben/konstellation` zeigt vier räumlich getrennte, getönte Cluster mit Kapitel-Labels.
- [ ] Innerhalb eines Clusters liegen inhaltlich ähnliche Knoten nah beieinander (Stichprobe: `utilisation-*` im Handwerk-Cluster benachbart).
- [ ] Cluster-übergreifende Kanten sichtbar (z. B. `angst`↔`panik`, `burnout`↔`selbstfuersorge`).
- [ ] Hover/Fokus: Knoten hebt sich, zugehörige Kanten gold. `/erleben/hybrid` zusätzlich mit Drift/Highlight; `prefers-reduced-motion` stoppt Bewegung.
- [ ] Klick auf Knoten → richtige `/erleben/thema/<slug>`-Seite.
- [ ] Force-Graph (`/erleben/graph`) lädt weiterhin fehlerfrei mit vier Clustern.

- [ ] **Step 5: Commit**

```bash
git add site/src/content/themen
git commit -m "Erleben v2: K4-Fall- und neue Knoten-Summaries + Abnahme"
```

---

## Self-Review

**Spec coverage:**
- §3 Knoten-Set (50, remap+neu) → Task 1 (Manifest), Task 7 (Writer). ✓
- §4 NMDS-Pipeline (Korpus→TF-IDF→Dissim→NMDS→Placement→Kanten→Output) → Tasks 1–4. ✓
- §4 Kriterium TF-IDF-Kosinus → Task 2. ✓ Determinismus → Tasks 3/4/9. ✓
- §5 Datenmodell (CLUSTERS, Cluster-Typ, CLUSTER_META) → Task 6 (graph.ts) + Task 7 (config.ts). ✓
- §6 Rendering (Cluster-Hulls + Labels, nur Konstellation; Force untouched) → Task 8. ✓
- §7 Verifikation (graph.test.ts, Determinismus, build, astro check, manuell) → Tasks 6/9. ✓
- §8 Dateien → alle abgedeckt. ✓
- Kanten Ähnlichkeit+Kuratierung → Task 4 (Vorschläge) + Task 5 (Kuratierung). ✓

**Placeholder scan:** Keine „TBD/TODO"; alle Code-Schritte enthalten vollständigen Code. Summaries in Task 9 sind bewusst inhaltliche Handarbeit mit Beispiel. ✓

**Type consistency:** `Cluster`/`CLUSTER_META` (Task 6) ↔ `content.config.ts` CLUSTERS (Task 7) identisch k1..k4. `build()`-Rückgabe (Task 4) ↔ `write_frontmatter` liest `layout[slug]["cluster"/"x"/"y"]` konsistent. `REGIONS`-Keys = Cluster-IDs. `edges.curated.json`-Format `[a,b]` ↔ Writer/Validator konsistent. ✓
