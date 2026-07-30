# Psyche — Bischof-Konzeptkarte Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eine NMDS-Konzeptkarte aus Norbert Bischofs Kern-Theorie (Grundbuch + Theoretische Psychologie 2026) als dritter Karten-„Raum" `psyche` auf `/psyche`, nach exakt dem bestehenden `erleben`/`herausforderungen`-Muster.

**Architecture:** Die Pipeline (`scripts/nmds-layout/`) ist bereits raum-parametrisiert über `spaces.py` (Env `SPACE`); die Rechenskripte (`build_layout.py`, `curate_edges.py`, `sync_content.py`, `extract_corpus.py`, `tfidf.py`, `nmds.py`) bleiben unverändert. Neu sind: (1) ein `_psyche()`-Raum in `spaces.py` inkl. Regionen für 5 Cluster, (2) die Bischof-Content-Erzeugung (PDF→Passagen-Chunks→kuratierte Konzept-Knoten→Passagen-Retrieval→Knotenordner), (3) die dritte Kopie der Site-Karten-Seiten (`psyche` Collection + Cluster-Meta + Seiten).

> **Pivot 2026-07-30 (Task 2 Fix-Loop):** Ursprünglich waren „Kapitel-Chunks" als Retrieval-Einheit geplant. In den real extrahierten PDFs stehen Kapitel-Nummer und -Titel jedoch auf getrennten Zeilen, die zwei Bücher nutzen verschiedene Formate, und ToC/Fußnoten verrauschen die Heading-Erkennung — ein zuverlässiger Kapitel-Parser ist teuer und fragil. Da die Chunk-Labels ohnehin nie live gehen (`quelle.md` ist lokale TF-IDF-Quelle; die publizierte Zusammenfassung wird in Task 9 von Hand geschrieben), zählt nur sauberer, konzept-relevanter **Text**. Entscheidung des Nutzers: **Passagen-Chunks** (~200-Wort-Fenster an Absatzgrenzen, Seiten-Möblierung entfernt). Task 2 und die `score_chunks`/`write_folders`-Signaturen in Task 4 sind entsprechend angepasst; Task 9 bleibt unberührt.

**Tech Stack:** Python 3 (numpy, stdlib; `pdftotext` CLI), Astro 7 Content Collections, TypeScript, vitest, pytest.

## Global Constraints

- **Bibliothek ist gitignored** (`Bibliothek/*` außer README): PDFs, `_extracted/`, und alle `quelle.md`-Rohpassagen bleiben LOKAL, gehen NICHT nach GitHub/Netlify.
- **Urheberrecht:** In `site/src/content/psyche/` (committet, live) gehen NUR eigene Zusammenfassungen (`meta.json.summary`, optional `text.md`) — KEINE verbatim Buchpassagen. `quelle.md` dient ausschließlich der TF-IDF-Positionsberechnung.
- **Determinismus:** NMDS `seed=42`, idempotente Rebuilds (bestehende Pipeline-Garantie) bleiben erhalten.
- **Regression:** Die `erleben`- und `herausforderungen`-Karten dürfen nicht brechen. Default `SPACE=erleben` muss byte-identisch bleiben (`out_suffix=""`).
- **Knoten-Ziel:** 40–60 Konzept-Knoten. **Cluster:** 5 (`p1`–`p5`).
- **Cluster-IDs `p1`–`p5`** müssen an DREI Stellen identisch sein: `scripts/nmds-layout/spaces.py`, `site/src/content.config.ts` (`PSYCHE_CLUSTERS`), `site/src/lib/graph.ts` (`PSYCHE_CLUSTER_META`).
- **Cluster-Labels/-Farben:**
  - `p1` — „Wissenschaft & Erkenntnis" — `--ink-2`
  - `p2` — „Motivation (Zürcher Modell)" — `--marker`
  - `p3` — „Kognition & Wahrnehmung" — `--leaf`
  - `p4` — „Emotion & Affekt" — `--sun-deep`
  - `p5` — „System & Kybernetik" — `--ink-3`
- **Python ausführen** aus `scripts/nmds-layout/`; venv falls vorhanden: `./.venv/bin/python`, sonst `python3`. Tests: `python3 -m pytest tests/ -v` (aus `scripts/nmds-layout/`).
- **Site-Build/Tests** aus `site/`: `npm run build`, `npx vitest run`.

---

## File Structure

**Neu (Pipeline):**
- `scripts/nmds-layout/extract_pdf.py` — PDF→Text (`pdftotext`) für die 2 Bücher nach `_extracted/`.
- `scripts/nmds-layout/book_chunks.py` — zerlegt extrahierten Text in Passagen-Chunks `{text}` (~200-Wort-Fenster, Seiten-Möblierung entfernt).
- `scripts/nmds-layout/retrieve_passages.py` — ordnet je Konzept die Top-K Passagen-Chunks zu, schreibt Knotenordner (`quelle.md` + `meta.json`).
- `scripts/nmds-layout/psyche_manifest.py` — kuratierte Konzept-Knoten (`slug, cluster, headings, title, terms`).
- `scripts/nmds-layout/tests/test_book_chunks.py`, `tests/test_retrieve.py`, `tests/test_psyche_space.py`.

**Modifiziert (Pipeline):**
- `scripts/nmds-layout/spaces.py` — `_grid_regions()` Helfer + `_psyche()`-Raum.

**Neu (Bibliothek, gitignored):**
- `Bibliothek/Allgemeine Psychologie Materials/_extracted/*.txt`
- `Bibliothek/Allgemeine Psychologie/<seq>-<slug>/{quelle.md,meta.json}`

**Modifiziert (Site):**
- `site/src/content.config.ts` — `PSYCHE_CLUSTERS` + `psyche` Collection.
- `site/src/lib/graph.ts` — `PSYCHE_CLUSTER_META` + `CollectionName` um `'psyche'` erweitern.
- `site/src/pages/[teil].astro` — `psyche` aus dem Platzhalter-Filter ausschließen.
- `site/src/lib/graph.test.ts` — Test für `PSYCHE_CLUSTER_META`.

**Neu (Site):**
- `site/src/pages/psyche/index.astro` — Kartenseite (Klon von `herausforderungen/index.astro`).
- `site/src/pages/psyche/thema/[slug].astro` — Detailseite (Klon von `herausforderungen/thema/[slug].astro`).
- `site/src/content/psyche/<slug>/index.md` — generierter Content (via `sync_content.py`).

---

## Phasenschnitt

- **Phase A** (Task 1–4): Content-Erzeugung bis Knotenordner stehen.
- **Phase B** (Task 5–6): Raum-Wiring + Layout, **Reality-Check-Gate** (Stress + inhaltliche Sicht) BEVOR Site-Umbau.
- **Phase C** (Task 7–9): Site-Integration + Build-Gate + Deploy.

---

### Task 1: PDF-Extraktion

**Files:**
- Create: `scripts/nmds-layout/extract_pdf.py`
- Output (gitignored): `Bibliothek/Allgemeine Psychologie Materials/_extracted/grundbuch.txt`, `.../theoretische-psychologie.txt`

**Interfaces:**
- Produces: `_extracted/<key>.txt` (UTF-8, Seiten mit `\f`-Trenner von `pdftotext`), `key ∈ {grundbuch, theoretische-psychologie}`.

- [ ] **Step 1: Skript schreiben**

```python
# scripts/nmds-layout/extract_pdf.py
"""Extrahiert die 2 Bischof-Kern-Bücher via pdftotext nach _extracted/ (gitignored).
Nur Textschicht (mit pdftotext verifiziert, kein OCR)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
MAT = os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie Materials")
OUT = os.path.join(MAT, "_extracted")

BOOKS = {
    "grundbuch": "Bischof Grundbuch.pdf",
    "theoretische-psychologie": "Bischof_2026_Theoretische-Psychologie.pdf",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for key, fname in BOOKS.items():
        src = os.path.join(MAT, fname)
        dst = os.path.join(OUT, f"{key}.txt")
        subprocess.run(["pdftotext", "-enc", "UTF-8", src, dst], check=True)
        n = len(open(dst, encoding="utf-8").read())
        print(f"{key}: {n} Zeichen -> {dst}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Ausführen**

Run: `cd scripts/nmds-layout && python3 extract_pdf.py`
Expected: zwei Dateien, je > 500.000 Zeichen; keine Exception.

- [ ] **Step 3: Sichtprüfung**

Run: `head -c 400 "../../Bibliothek/Allgemeine Psychologie Materials/_extracted/grundbuch.txt"`
Expected: lesbarer Fließtext mit Kapitelnummern (z. B. „1.1.1 …").

- [ ] **Step 4: Commit** (nur das Skript — `_extracted/` ist gitignored)

```bash
git add scripts/nmds-layout/extract_pdf.py
git commit -m "psyche: PDF-Extraktion der Bischof-Kern-Bücher"
```

---

### Task 2: Passagen-Chunker

Zerlegt den extrahierten Buchtext in robuste Passagen-Fenster (~200 Wörter, an Absatzgrenzen) — die Retrieval-Einheit. Seiten-Möblierung (Export-Timestamp, `.indb`-Footer, reine Seitenzahlen, Form-Feed) wird VOR dem Fenstern entfernt, damit sie den TF-IDF-Corpus nicht verrauscht. (Pivot weg von Kapitel-Chunks — siehe Architecture-Notiz.)

**Files:**
- Create/overwrite: `scripts/nmds-layout/book_chunks.py`
- Create/overwrite: `scripts/nmds-layout/tests/test_book_chunks.py`

**Interfaces:**
- Produces: `passages(text: str, target_words: int = 200) -> list[dict]` mit `{"text": str}`. Zerlegt an Leerzeilen in Absätze; entfernt Rausch-Zeilen; akkumuliert Absätze bis ~`target_words`, dann neuer Chunk.
- Produces: `all_passages(extracted_dir: str) -> list[dict]` — Passagen beider Bücher, je mit zusätzlichem `"book"`-Key.
- Produces: `_clean_lines(text: str)` — Generator über Zeilen ohne Seiten-Möblierung (intern, aber getestet).

- [ ] **Step 1: Failing test schreiben**

```python
# scripts/nmds-layout/tests/test_book_chunks.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from book_chunks import passages, _clean_lines

SAMPLE = """13.01.2014 14:59:54
Erster Absatz über Wahrnehmung und Farbe.
00 Grundkurs Psychologie (Bischof).indb 5

Zweiter Absatz über Motivation und Sollwert.

123
Dritter Absatz über Regelkreise.
"""


def test_entfernt_seiten_moeblierung():
    joined = "\n".join(_clean_lines(SAMPLE))
    assert "13.01.2014" not in joined          # Export-Timestamp weg
    assert ".indb" not in joined               # Footer weg
    assert "\n123\n" not in "\n" + joined + "\n"  # reine Seitenzahl weg
    assert "Wahrnehmung" in joined             # echter Text bleibt


def test_fenstert_nach_wortzahl():
    text = "\n\n".join(f"Absatz {i} " + "wort " * 60 for i in range(5))
    chs = passages(text, target_words=100)
    assert len(chs) >= 2                        # 5×~61 Wörter -> mehrere Fenster
    assert all(c["text"].strip() for c in chs)


def test_kurzer_text_ein_chunk():
    chs = passages("Nur ein kurzer Absatz.", target_words=200)
    assert len(chs) == 1 and "kurzer" in chs[0]["text"]


if __name__ == "__main__":
    test_entfernt_seiten_moeblierung()
    test_fenstert_nach_wortzahl()
    test_kurzer_text_ein_chunk()
    print("OK test_book_chunks")
```

- [ ] **Step 2: Test ausführen (rot)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_book_chunks.py -v`
Expected: FAIL (`ModuleNotFoundError: book_chunks` bzw. `ImportError: passages`).

- [ ] **Step 3: Implementierung schreiben**

```python
# scripts/nmds-layout/book_chunks.py
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
```

- [ ] **Step 4: Test ausführen (grün)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_book_chunks.py -v`
Expected: PASS (3 Tests).

- [ ] **Step 5: Reale Passagen prüfen (Gate)**

Run: `cd scripts/nmds-layout && python3 -c "from book_chunks import all_passages; import os; d=os.path.join('..','..','Bibliothek','Allgemeine Psychologie Materials','_extracted'); c=all_passages(d); ws=[len(x['text'].split()) for x in c]; print(len(c),'Passagen; Ø Wörter=%d'%(sum(ws)//len(ws))); j=' '.join(x['text'] for x in c[:50]); print('kein Timestamp:', '13.01.2014' not in j)"`
Expected: einige hundert bis wenige tausend Passagen, Ø ~200 Wörter, „kein Timestamp: True".

- [ ] **Step 6: Commit**

```bash
git add scripts/nmds-layout/book_chunks.py scripts/nmds-layout/tests/test_book_chunks.py
git commit -m "psyche: Passagen-Chunker für Bischof-Bücher (TDD, Pivot von Kapitel-Chunks)"
```

---

### Task 3: Konzept-Extraktion & kuratiertes Manifest

Hybrid: automatischer Konzept-Vorschlag aus den Chunks, dann kuratierte Endliste. Dies ist ein **LLM+Kuration-Task**, kein reiner Code-Task — Deliverable ist die Datei `psyche_manifest.py`.

**Files:**
- Create: `scripts/nmds-layout/psyche_manifest.py`
- Create (temporär, gitignored): `Bibliothek/Allgemeine Psychologie Materials/_extracted/_concepts_draft.json`

**Interfaces:**
- Produces: `psyche_manifest.py` exportiert `NODES = [{"slug","cluster","headings","title","terms"}, …]`.
  - `slug`: kebab-case, eindeutig.
  - `cluster`: eines von `p1..p5`.
  - `headings`: `[str(seq)]` — laufende Nummer 1..N, EINDEUTIG (bildet den Ordner `<seq>-<slug>`; wird von `extract_corpus.folder_name`/`toc_number` konsumiert).
  - `title`: Anzeigename.
  - `terms`: `list[str]` — Retrieval-Suchbegriffe/Aliase des Konzepts (für Task 4).

- [ ] **Step 1: Auto-Vorschlag erzeugen**

Konzept-Extraktion über die Passagen-Chunks (Stichprobe von Passagen-Texten aus beiden Büchern). Nutze einen Extraktions-Prompt (LLM) mit exakt dieser Aufgabe:

> „Du erhältst Textpassagen aus Norbert Bischofs *Grundbuch* und *Theoretische Psychologie*. Extrahiere 40–60 zentrale, benannte Konzepte seiner Theorie (z. B. Zürcher Modell der sozialen Motivation, Sicherheitssystem, Erregungssystem, Autonomiesystem, Sollwert-Regulation, appetitiv/aversiv, Coping, Prägung, Objektivierung, …). Gib JSON zurück: Liste von `{slug, title, cluster, terms}`. `cluster` ist eines von: p1=Wissenschaft & Erkenntnis, p2=Motivation (Zürcher Modell), p3=Kognition & Wahrnehmung, p4=Emotion & Affekt, p5=System & Kybernetik. `terms` = 3–8 deutsche Suchbegriffe/Aliase, unter denen das Konzept im Buchtext vorkommt. Keine erfundenen Konzepte; nur was bei Bischof vorkommt."

Speichere die JSON-Antwort nach `_extracted/_concepts_draft.json`.

- [ ] **Step 2: Kuratieren**

Der Nutzer (bzw. der ausführende Agent gemeinsam mit dem Nutzer) redigiert `_concepts_draft.json`: Dubletten zusammenführen, unklare Konzepte streichen, Cluster-Zuordnung prüfen, auf 40–60 Knoten bringen, Cluster `p1..p5` je mit ≥3 Knoten füllen.

- [ ] **Step 3: `psyche_manifest.py` generieren**

Aus dem kuratierten JSON die Manifest-Datei schreiben (laufende, eindeutige `headings`-Nummern vergeben). Zielformat (Beispiel mit 2 Knoten, real 40–60):

```python
# scripts/nmds-layout/psyche_manifest.py
# Kuratierte Bischof-Konzepte. headings = laufende Nummer (Ordner <seq>-<slug>).
# terms = Retrieval-Suchbegriffe (Task 4). Cluster p1..p5 (siehe spaces.py).
_RAW = [
    # (slug, cluster, seq, title, terms)
    ("zuercher-modell", "p2", "1", "Zürcher Modell der sozialen Motivation",
     ["zürcher modell", "soziale motivation", "sicherheit", "erregung", "autonomie"]),
    ("sollwert-regulation", "p5", "2", "Sollwert-Regulation",
     ["sollwert", "istwert", "regelkreis", "regulation", "homöostase"]),
    # … 40–60 Einträge total …
]
NODES = [{"slug": s, "cluster": c, "headings": [h], "title": t, "terms": terms}
         for (s, c, h, t, terms) in _RAW]
```

- [ ] **Step 4: Manifest-Form validieren**

Run:
```bash
cd scripts/nmds-layout && python3 -c "
from psyche_manifest import NODES
slugs=[n['slug'] for n in NODES]; seqs=[n['headings'][0] for n in NODES]
assert 40<=len(NODES)<=60, len(NODES)
assert len(set(slugs))==len(slugs), 'slugs nicht eindeutig'
assert len(set(seqs))==len(seqs), 'seq-Nummern nicht eindeutig'
from collections import Counter; cl=Counter(n['cluster'] for n in NODES)
assert set(cl)<= {'p1','p2','p3','p4','p5'}, cl
assert all(v>=3 for v in cl.values()), cl
assert all(n['terms'] for n in NODES), 'terms fehlen'
print('OK', len(NODES), 'Knoten', dict(cl))
"
```
Expected: `OK <N> Knoten {…}` ohne AssertionError.

- [ ] **Step 5: Commit** (Manifest ist Code, geht ins Repo; `_concepts_draft.json` ist gitignored)

```bash
git add scripts/nmds-layout/psyche_manifest.py
git commit -m "psyche: kuratiertes Bischof-Konzept-Manifest (40–60 Knoten, p1–p5)"
```

---

### Task 4: Passagen-Retrieval → Knotenordner

Ordnet jedem Konzept die inhaltlich passenden **Kapitel-Chunks** zu und schreibt die Knotenordner. `quelle.md` bleibt lokal (TF-IDF-Quelle); `meta.json` liefert den (später zu redigierenden) `summary`.

**Files:**
- Create: `scripts/nmds-layout/retrieve_passages.py`
- Test: `scripts/nmds-layout/tests/test_retrieve.py`
- Output (gitignored): `Bibliothek/Allgemeine Psychologie/<seq>-<slug>/{quelle.md,meta.json}`

**Interfaces:**
- Consumes: `psyche_manifest.NODES` (mit `terms`), `book_chunks.all_passages`, `extract_corpus.folder_name`.
- Produces: `score_chunks(terms: list[str], chunks: list[dict]) -> list[tuple[int, float]]` — (chunk_index, score) absteigend, Score = Summe der (case-insensitiven) Term-Vorkommen in `text`, längen-normiert (pro 1000 Wörter). (Chunks haben nur noch `text`/`book`, keinen Titel.)
- Produces: `retrieve(nodes, chunks, top_k=6) -> dict[str, list[int]]` — je slug die Top-K Chunk-Indizes (Score>0).
- Produces: `write_folders(bib_dir, nodes, chunks, assign)` — schreibt `quelle.md` (konkatenierte Passagen-Texte) + `meta.json` (`title`, `summary`-Platzhalter, `status:"stub"`).

- [ ] **Step 1: Failing test schreiben**

```python
# scripts/nmds-layout/tests/test_retrieve.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from retrieve_passages import score_chunks, retrieve

CHUNKS = [
    {"text": "Der Sollwert steuert den Regelkreis. Sollwert überall.", "book": "b"},
    {"text": "Farbe und Form der Wahrnehmung.", "book": "b"},
    {"text": "Ein Satz ohne Treffer hier.", "book": "b"},
]


def test_score_normiert():
    sc = dict(score_chunks(["sollwert", "regelkreis"], CHUNKS))
    assert sc[0] > sc[1], sc          # Chunk 0 trifft, Chunk 1 nicht
    assert sc[2] == 0.0


def test_retrieve_top_k_nur_positive():
    nodes = [{"slug": "x", "terms": ["sollwert"]}, {"slug": "y", "terms": ["nichttreffer"]}]
    a = retrieve(nodes, CHUNKS, top_k=2)
    assert a["x"] == [0]               # nur Chunk 0 hat Score>0
    assert a["y"] == []                # kein Treffer -> leer


if __name__ == "__main__":
    test_score_normiert()
    test_retrieve_top_k_nur_positive()
    print("OK test_retrieve")
```

- [ ] **Step 2: Test ausführen (rot)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_retrieve.py -v`
Expected: FAIL (`ModuleNotFoundError: retrieve_passages`).

- [ ] **Step 3: Implementierung schreiben**

```python
# scripts/nmds-layout/retrieve_passages.py
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
```

- [ ] **Step 4: Test ausführen (grün)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_retrieve.py -v`
Expected: PASS (2 Tests).

- [ ] **Step 5: Ordner real erzeugen**

Run: `cd scripts/nmds-layout && python3 retrieve_passages.py`
Expected: „<N> Knotenordner geschrieben; ohne Treffer: keine". Falls Knoten ohne Treffer → deren `terms` in `psyche_manifest.py` schärfen (Task 3, Step 3) und erneut ausführen.

- [ ] **Step 6: Corpus-Länge prüfen (Gate)**

Run:
```bash
cd scripts/nmds-layout && python3 -c "
import os, glob
bib=os.path.join('..','..','Bibliothek','Allgemeine Psychologie')
short=[]
for d in sorted(glob.glob(os.path.join(bib,'*'))):
    q=os.path.join(d,'quelle.md')
    w=len(open(q,encoding='utf-8').read().split()) if os.path.exists(q) else 0
    if w<40: short.append((os.path.basename(d), w))
print('zu kurz (<40 Wörter):', short or 'keine')
"
```
Expected: „keine". Andernfalls `terms`/`top_k` anpassen.

- [ ] **Step 7: Commit** (nur Code; Knotenordner sind gitignored)

```bash
git add scripts/nmds-layout/retrieve_passages.py scripts/nmds-layout/tests/test_retrieve.py
git commit -m "psyche: Passagen-Retrieval (Kapitel-Chunks) + Knotenordner (TDD)"
```

---

### Task 5: `psyche`-Raum in `spaces.py` (Regionen für 5 Cluster)

Der einzige Eingriff in den Pipeline-Kern: dritter Raum + Regionen-Grid (heute nur 4 Quadranten).

**Files:**
- Modify: `scripts/nmds-layout/spaces.py`
- Test: `scripts/nmds-layout/tests/test_psyche_space.py`

**Interfaces:**
- Consumes: `psyche_manifest.NODES`.
- Produces: `get_space("psyche")` liefert Dict mit `name="psyche"`, `bib_dir=…/Bibliothek/Allgemeine Psychologie`, `themen_dir=…/site/src/content/psyche`, `nodes`, `clusters=("p1",…,"p5")`, `regions` (Grid), `out_suffix=".psyche"`.
- Produces: `_grid_regions(ids, cols)` — `{id: (x0,x1,y0,y1)}`, alle in `[5,95]`, disjunkt.

- [ ] **Step 1: Failing test schreiben**

```python
# scripts/nmds-layout/tests/test_psyche_space.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from spaces import get_space, _grid_regions


def test_grid_regionen_im_canvas_und_disjunkt():
    r = _grid_regions(("p1", "p2", "p3", "p4", "p5"), cols=3)
    assert set(r) == {"p1", "p2", "p3", "p4", "p5"}
    for (x0, x1, y0, y1) in r.values():
        assert 5 <= x0 < x1 <= 95 and 5 <= y0 < y1 <= 95


def test_psyche_space_konfiguration():
    sp = get_space("psyche")
    assert sp["name"] == "psyche"
    assert sp["clusters"] == ("p1", "p2", "p3", "p4", "p5")
    assert sp["out_suffix"] == ".psyche"
    assert set(sp["regions"]) == set(sp["clusters"])
    assert sp["bib_dir"].endswith(os.path.join("Bibliothek", "Allgemeine Psychologie"))
    assert sp["themen_dir"].endswith(os.path.join("content", "psyche"))


def test_erleben_unveraendert():
    sp = get_space("erleben")
    assert sp["out_suffix"] == "" and sp["clusters"] == ("k1", "k2", "k3", "k4")


if __name__ == "__main__":
    test_grid_regionen_im_canvas_und_disjunkt()
    test_psyche_space_konfiguration()
    test_erleben_unveraendert()
    print("OK test_psyche_space")
```

- [ ] **Step 2: Test ausführen (rot)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_psyche_space.py -v`
Expected: FAIL (`ImportError: cannot import name '_grid_regions'`).

- [ ] **Step 3: `_grid_regions` + `_psyche()` ergänzen**

In `scripts/nmds-layout/spaces.py` nach der `_QUADRANTS`-Definition einfügen:

```python
import math

def _grid_regions(ids, cols=3):
    """Gleichmäßiges Grid im Canvas [5,95]² mit kleiner Lücke zwischen den Zellen."""
    n = len(ids)
    rows = math.ceil(n / cols)
    gap = 2.0
    cw = (90.0 - gap * (cols - 1)) / cols
    ch = (90.0 - gap * (rows - 1)) / rows
    out = {}
    for k, cid in enumerate(ids):
        r, c = divmod(k, cols)
        x0 = 5.0 + c * (cw + gap)
        y0 = 5.0 + r * (ch + gap)
        out[cid] = (round(x0, 2), round(x0 + cw, 2), round(y0, 2), round(y0 + ch, 2))
    return out
```

Und einen `_psyche()`-Raum analog zu `_herausforderungen()` hinzufügen:

```python
_PSYCHE_CLUSTERS = ("p1", "p2", "p3", "p4", "p5")
# Kanten-Schwellen (analog _EDGES_ERLEBEN; ~50-Knoten-Karte, in Task 6 nachjustierbar).
_EDGES_PSYCHE = {"cross_min_sim": 0.10, "cross_topk": 40, "curate_min_sim": 0.20, "curate_max_deg": 3}

def _psyche():
    try:
        from psyche_manifest import NODES as _PN
    except Exception:
        _PN = []
    return {
        "name": "psyche",
        "bib_dir": os.path.join(ROOT, "Bibliothek", "Allgemeine Psychologie"),
        "themen_dir": os.path.join(ROOT, "site", "src", "content", "psyche"),
        "nodes": _PN,
        "clusters": _PSYCHE_CLUSTERS,
        "regions": _grid_regions(_PSYCHE_CLUSTERS, cols=3),
        "out_suffix": ".psyche",
        "edges": _EDGES_PSYCHE,
    }
```

> Hinweis: Der `"edges"`-Key kam durch den herausforderungen-Refactor hinzu (`build_layout.py`/`curate_edges.py` lesen `SPACE["edges"][...]`). Ohne ihn wirft `SPACE=psyche` in Task 6 einen KeyError. Der Test (Step 1) prüft daher `get_space("psyche")["edges"]` auf die vier Schlüssel.

In `get_space` den Zweig ergänzen (vor dem `raise`):

```python
    if name == "psyche":
        return _psyche()
```

Und die Fehlermeldung erweitern: `(erlaubt: erleben | herausforderungen | psyche)`.

- [ ] **Step 4: Test ausführen (grün)**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/test_psyche_space.py -v`
Expected: PASS (3 Tests).

- [ ] **Step 5: Regression — bestehende Tests grün**

Run: `cd scripts/nmds-layout && python3 -m pytest tests/ -v`
Expected: alle Tests PASS (inkl. `test_corpus`, `test_layout`, `test_nmds`, `test_tfidf`).

- [ ] **Step 6: Commit**

```bash
git add scripts/nmds-layout/spaces.py scripts/nmds-layout/tests/test_psyche_space.py
git commit -m "psyche: dritter Raum in spaces.py + Grid-Regionen für 5 Cluster (TDD)"
```

---

### Task 6: Layout rechnen + Reality-Check-Gate

Bestehende Pipeline unter `SPACE=psyche` laufen lassen. **Gate vor Phase C.**

**Files:**
- Output (gitignored): `scripts/nmds-layout/out/layout.psyche.json`, `out/edges.suggested.psyche.json`, `out/edges.curated.psyche.json`

- [ ] **Step 1: Layout + Kanten rechnen**

Run:
```bash
cd scripts/nmds-layout && SPACE=psyche python3 build_layout.py && SPACE=psyche python3 curate_edges.py
```
Expected: `[psyche] layout.psyche.json: <N> Knoten; <M> Kanten-Vorschläge` und `edges.curated.psyche.json: <K> Kanten; Knoten ohne Kante: keine`.

- [ ] **Step 2: NMDS-Stress prüfen**

Run:
```bash
cd scripts/nmds-layout && SPACE=psyche python3 -c "
from spaces import SPACE, NODES
from extract_corpus import build_corpus_from_folders
from tfidf import tfidf_matrix, cosine_dissim
from nmds import nmds
corpus=build_corpus_from_folders(SPACE['bib_dir'])
for cl in SPACE['clusters']:
    slugs=[n['slug'] for n in NODES if n['cluster']==cl]
    if len(slugs)<2: continue
    m=tfidf_matrix([corpus[s] for s in slugs])
    _,s=nmds(cosine_dissim(m), seed=42)
    print(cl, 'stress=%.3f'%s, len(slugs),'Knoten')
"
```
Expected: Stress je Cluster möglichst < ~0.2. Deutlich höher → `terms`/Knoten in Task 3 revidieren, Task 4+6 wiederholen.

- [ ] **Step 3: Inhaltlicher Reality-Check (menschlich)**

Layout-Positionen sichten: liegen thematisch verwandte Konzepte nah beieinander? Bei Unplausibilität zurück zu Task 3 (Konzepte/Cluster) bzw. Task 4 (`terms`/`top_k`). **Erst weiter zu Phase C, wenn die Karte inhaltlich Sinn ergibt.**

- [ ] **Step 4: Kein Commit** (nur gitignored Output). Notiz im nächsten Commit.

---

### Task 7: Site — `psyche` Collection + Cluster-Meta

**Files:**
- Modify: `site/src/content.config.ts`
- Modify: `site/src/lib/graph.ts`
- Modify: `site/src/lib/graph.test.ts`

**Interfaces:**
- Consumes: nichts Neues.
- Produces: `collections.psyche` (Schema `PSYCHE_CLUSTERS`); `PSYCHE_CLUSTER_META: ClusterMeta[]`; `CollectionName` inkl. `'psyche'`.

- [ ] **Step 1: Failing test schreiben**

In `site/src/lib/graph.test.ts` ergänzen (neuer `it`-Block innerhalb `describe('assembleGraph', …)`):

```typescript
import { assembleGraph, PSYCHE_CLUSTER_META, type RawNode } from './graph';

  it('liefert die fünf Psyche-Cluster-Metadaten', () => {
    const p = (slug: string): RawNode => ({
      slug, title: slug, cluster: 'p1', summary: 's', x: 10, y: 20, status: 'stub', related: [],
    });
    const g = assembleGraph([p('a')], PSYCHE_CLUSTER_META);
    expect(g.clusters.map((c) => c.id)).toEqual(['p1', 'p2', 'p3', 'p4', 'p5']);
    expect(g.clusters[1]).toMatchObject({ id: 'p2', colorVar: '--marker' });
  });
```

- [ ] **Step 2: Test ausführen (rot)**

Run: `cd site && npx vitest run src/lib/graph.test.ts`
Expected: FAIL (`PSYCHE_CLUSTER_META` nicht exportiert).

- [ ] **Step 3: `graph.ts` erweitern**

In `site/src/lib/graph.ts` nach `HERAUS_CLUSTER_META` einfügen:

```typescript
// Raum „Psyche: Was wir sind" (Bischof, Allgemeine Psychologie).
export const PSYCHE_CLUSTER_META: ClusterMeta[] = [
  { id: 'p1', label: 'Wissenschaft & Erkenntnis', colorVar: '--ink-2' },
  { id: 'p2', label: 'Motivation (Zürcher Modell)', colorVar: '--marker' },
  { id: 'p3', label: 'Kognition & Wahrnehmung', colorVar: '--leaf' },
  { id: 'p4', label: 'Emotion & Affekt', colorVar: '--sun-deep' },
  { id: 'p5', label: 'System & Kybernetik', colorVar: '--ink-3' },
];
```

Und `CollectionName` erweitern:

```typescript
export type CollectionName = 'themen' | 'herausforderungen' | 'psyche';
```

- [ ] **Step 4: `content.config.ts` erweitern**

In `site/src/content.config.ts`: `PSYCHE_CLUSTERS` neben den anderen Cluster-Konstanten ergänzen, Collection definieren, in `collections` aufnehmen:

```typescript
export const PSYCHE_CLUSTERS = ['p1', 'p2', 'p3', 'p4', 'p5'] as const;
```
```typescript
const psyche = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './src/content/psyche', generateId: slugFromIndex }),
  schema: ({ image }) => themaSchema(PSYCHE_CLUSTERS, image),
});

export const collections = { themen, herausforderungen, psyche };
```

- [ ] **Step 5: Test ausführen (grün)**

Run: `cd site && npx vitest run src/lib/graph.test.ts`
Expected: PASS (alle Blöcke, inkl. neuem Psyche-Block).

- [ ] **Step 6: Commit**

```bash
git add site/src/content.config.ts site/src/lib/graph.ts site/src/lib/graph.test.ts
git commit -m "psyche: Collection + PSYCHE_CLUSTER_META (TDD)"
```

---

### Task 8: Site — Karten- & Detailseite für `/psyche`

Dritte Kopie des `herausforderungen`-Seitentemplates.

**Files:**
- Create: `site/src/pages/psyche/index.astro`
- Create: `site/src/pages/psyche/thema/[slug].astro`
- Modify: `site/src/pages/[teil].astro`

**Interfaces:**
- Consumes: `buildGraph('psyche', PSYCHE_CLUSTER_META)`, `getCollection('psyche')`.

- [ ] **Step 1: `psyche/index.astro` erstellen** (Klon von `herausforderungen/index.astro`, drei Ersetzungen)

```astro
---
import Site from '../../layouts/Site.astro';
import GraphKonstellation from '../../components/graph/GraphKonstellation.astro';
import { buildGraph, PSYCHE_CLUSTER_META } from '../../lib/graph';
import { PARTS } from '../../site';

const part = PARTS.find((p) => p.id === 'psyche')!;
const graph = await buildGraph('psyche', PSYCHE_CLUSTER_META);
---
<Site title={part.label} current="psyche">
  <section class="pagehead wrap">
    <p class="overline">{part.overline}</p>
    <h1>{part.label}</h1>
    <svg class="strich" viewBox="0 0 220 14" aria-hidden="true" focusable="false">
      <path d={part.strich} fill="none" stroke-width="4" stroke-linecap="round"></path>
    </svg>
  </section>
  <section class="wrap karte-stage">
    <GraphKonstellation
      graph={graph}
      basePath="/psyche/thema"
      ariaLabel="Karte der Psyche: Was wir sind (nach Norbert Bischof)"
    />
  </section>
</Site>

<style>
  .karte-stage :global(.konstellation.dim .node) { opacity: .25; transition: opacity .2s var(--ease); }
  .karte-stage :global(.konstellation.dim .node.hot) { opacity: 1; }
  .karte-stage :global(.konstellation.dim line) { stroke: var(--hairline); }
  .karte-stage :global(.konstellation.dim line.hot) { stroke: var(--sun-deep); stroke-width: .9; }
</style>

<script>
  const wrap = document.querySelector<HTMLElement>('.karte-stage .konstellation');
  if (wrap) {
    const nodes = Array.from(wrap.querySelectorAll<HTMLElement>('.node'));
    const lines = Array.from(wrap.querySelectorAll<SVGLineElement>('line'));
    const neighbors = new Map<string, Set<string>>();
    lines.forEach((l) => {
      const a = l.dataset.a!, b = l.dataset.b!;
      (neighbors.get(a) ?? neighbors.set(a, new Set()).get(a)!).add(b);
      (neighbors.get(b) ?? neighbors.set(b, new Set()).get(b)!).add(a);
    });
    const highlight = (slug: string | null) => {
      wrap.classList.toggle('dim', slug !== null);
      const hot = slug ? new Set([slug, ...(neighbors.get(slug) ?? [])]) : new Set<string>();
      nodes.forEach((n) => n.classList.toggle('hot', hot.has(n.dataset.slug!)));
      lines.forEach((l) => l.classList.toggle('hot', slug !== null && (l.dataset.a === slug || l.dataset.b === slug)));
    };
    nodes.forEach((n) => {
      n.addEventListener('mouseenter', () => highlight(n.dataset.slug!));
      n.addEventListener('focus', () => highlight(n.dataset.slug!));
      n.addEventListener('mouseleave', () => highlight(null));
      n.addEventListener('blur', () => highlight(null));
    });
  }
</script>
```

- [ ] **Step 2: `psyche/thema/[slug].astro` erstellen** — 1:1 Klon von `site/src/pages/herausforderungen/thema/[slug].astro`, dabei JEDES Vorkommen von `getCollection('herausforderungen')` → `getCollection('psyche')`, `current="herausforderungen"` → `current="psyche"`, und alle Href-Präfixe `/herausforderungen/thema/` → `/psyche/thema/` ersetzen. (Cluster-Meta dort wird aus `entry.data.cluster` via `PSYCHE_CLUSTER_META` aufgelöst — sicherstellen, dass die Datei `PSYCHE_CLUSTER_META` importiert, analog wie das Original `HERAUS_CLUSTER_META` nutzt.)

Zuerst das Original lesen und exakt spiegeln:
Run: `cat site/src/pages/herausforderungen/thema/'[slug]'.astro`

- [ ] **Step 3: `[teil].astro` Filter erweitern**

In `site/src/pages/[teil].astro` die `getStaticPaths`-Filterzeile ändern:

```typescript
    .filter((p) => p.id !== 'erleben' && p.id !== 'herausforderungen' && p.id !== 'psyche')
```

(Damit rendert `/psyche` die neue Kartenseite statt des generischen Platzhalters.)

- [ ] **Step 4: Build prüfen**

Run: `cd site && npm run build`
Expected: Build grün; Routen `/psyche`, `/psyche/thema/<slug>` werden generiert (in der Ausgabe sichtbar).

- [ ] **Step 5: Commit**

```bash
git add site/src/pages/psyche site/src/pages/'[teil].astro'
git commit -m "psyche: Karten- und Detailseite für /psyche (Klon des heraus-Templates)"
```

---

### Task 9: Content generieren + Build-Gate + Deploy

**Files:**
- Output (committet, live): `site/src/content/psyche/<slug>/index.md`

**Interfaces:**
- Consumes: `out/layout.psyche.json`, `out/edges.curated.psyche.json`, Knotenordner-`meta.json`/`text.md`.

- [ ] **Step 1: Summaries redigieren (Urheberrecht!)**

Die `meta.json.summary` jedes Knotens (aktuell TODO-Platzhalter) in **eigene Worte** fassen — KEINE verbatim Buchpassagen. Optional pro Knoten `text.md` (eigener Fließtext) anlegen. `status` auf `"full"` setzen, wo Text fertig ist. (Quelle zum Nachlesen: die lokale `quelle.md` im selben Ordner.)

- [ ] **Step 2: Content generieren**

Run: `cd scripts/nmds-layout && SPACE=psyche python3 sync_content.py`
Expected: „Content generiert: <N> Seiten, … Mediendateien kopiert". Erzeugt `site/src/content/psyche/<slug>/index.md` mit `cluster: pX`, `x/y`, `related`.

- [ ] **Step 3: Verifizieren, dass keine Rohpassagen live gehen**

Run:
```bash
cd /Users/sevi/Claude/Psyche_Now && grep -rl "TODO: eigene Zusammenfassung" site/src/content/psyche/ || echo "keine Platzhalter mehr"
```
Expected: „keine Platzhalter mehr" (sonst Step 1 nachholen).

- [ ] **Step 4: Build-Gate (Regression + neue Karte)**

Run:
```bash
cd site && npx vitest run && npm run build
```
Expected: alle vitest-Tests PASS; Astro-Build grün mit `/psyche`-Routen. Schema-Validierung (x∈[0,100], cluster∈p1..p5) muss durchlaufen.

- [ ] **Step 5: Commit**

```bash
git add site/src/content/psyche
git commit -m "psyche: generierter Bischof-Kartencontent (/psyche live)"
```

- [ ] **Step 6: Deploy**

Run: `git push`
Expected: Netlify Auto-Deploy auf `main`; nach Build `/psyche` live prüfen (Konstellation sichtbar, Knoten anklickbar → Detailseite).

---

## Self-Review

**Spec-Abdeckung:**
- Buch-Umfang (2 Kern-Bücher) → Task 1. ✎
- Hybrid-Konzepte (Auto→kuratiert) → Task 3. ✎
- Ansatz B / Kapitel-Chunk-Retrieval → Task 2 (Chunker) + Task 4 (Retrieval). ✎
- 40–60 Knoten, 5 Cluster → Task 3 (Validierung) + Global Constraints. ✎
- Karte auf `/psyche`, analog Muster → Task 7+8. ✎
- Multi-Map-Generalisierung → bereits vorhanden (`spaces.py`, Schema-Factory); nur Erweiterung Task 5+7+8. ✎
- Urheberrecht (Rohpassagen lokal, nur Summaries live) → Global Constraints + Task 4 (`quelle.md` gitignored) + Task 9 Step 1/3. ✎
- NMDS-Stress-Gate + Reality-Check → Task 6. ✎
- Build-Regression-Gate → Task 5 Step 5, Task 9 Step 4. ✎

**Platzhalter-Scan:** Die „TODO"-Zeichenkette in Task 4 ist ein absichtlicher, geprüfter Summary-Platzhalter (Gate in Task 9 Step 3 entfernt ihn) — kein Plan-Platzhalter. Sonst keine.

**Typ-Konsistenz:** `score_chunks`/`retrieve`/`write_folders` (Task 4) konsistent zwischen Test und Nutzung; `folder_name`/`toc_number` konsumieren `headings[0]` (Task 3 liefert eindeutige seq); `_grid_regions`/`get_space` (Task 5) konsistent mit Test; `PSYCHE_CLUSTER_META`/`PSYCHE_CLUSTERS`/`CollectionName` (Task 7) an allen drei Stellen `p1..p5`.
