# Psyche — Bischof-Konzeptkarte (Allgemeine Psychologie)

**Datum:** 2026-07-30
**Status:** Design bestätigt, bereit für Implementierungsplan
**Ziel:** Eine NMDS-Karte der zentralen Konzepte aus Norbert Bischofs Kern-Theorie,
integriert als eigene Konstellation auf der Hauptseite **Psyche** (`/psyche`) —
analog zur Hypnosystemik-Karte auf `/erleben`.

## Kontext & Ausgangslage

- Es existiert bereits eine vollständige NMDS-Pipeline unter `scripts/nmds-layout/`
  (TF-IDF → Kosinus-Distanz → nicht-metrisches SMACOF → Regionen-Fit/Relax → Kanten →
  Astro-Content). Sie erzeugt heute die Hypnosystemik-Karte aus 50 Knotenordnern.
- Die Site ist aktuell eine **Single-Map-Site**: die `themen`-Collection ist fest auf
  vier Cluster `k1–k4` in Quadranten verdrahtet
  (`site/src/content.config.ts`, `site/src/lib/graph.ts`,
  `site/src/components/graph/GraphKonstellation.astro`). Eine „Thema"-Dimension
  (Allgemeine Psychologie vs. Hypnosystemik) fehlt noch.
- Die drei Hauptseiten (`site/src/site.ts`): **psyche** · **herausforderungen** · **erleben**.
  `/erleben` hat bereits eine bespoke Graph-Seite (`erleben/index.astro`);
  `[teil].astro` filtert `erleben` deshalb heraus. `/psyche` ist heute ein Platzhalter,
  dessen Intro wörtlich das „allgemeinpsychologische Grundmodell (nach Norbert Bischof)"
  ankündigt — der natürliche Ort für diese Karte.

## Scope (bestätigte Weichenstellungen)

- **Buch-Umfang:** nur Kern-Theorie — `Bischof Grundbuch.pdf` +
  `Bischof_2026_Theoretische-Psychologie.pdf`. Beide haben eine saubere Textschicht
  (mit `pdftotext` verifiziert), kein OCR nötig. *Das Rätsel des Ödipus* und
  *Das Kraftfeld der Mythen* bleiben für eine spätere Ausbaustufe (nachrüstbar ohne
  Neuentwurf, nur mehr Passagen pro Knoten).
- **Knoten-Quelle:** hybrid — automatischer Konzept-Vorschlag, dann kuratierte Endliste.
- **Ansatz:** B — kuratierte Konzept-Knoten mit Passagen-Retrieval (nicht roher
  Buchtext, nicht Kapitel-als-Knoten).
- **Deliverable:** direkte Website-Integration als Konstellation auf `/psyche`.
- **Knotenzahl-Ziel:** ~40–60 Konzepte.
- **Cluster:** ~4–6 eigene thematische Cluster für Bischof (Vorschlag: Wissenschafts-/
  Erkenntnistheorie · Motivation / Zürcher Modell · Kognition / Wahrnehmung · Emotion ·
  Systemtheorie / Kybernetik). Endgültige Cluster ergeben sich aus der Kuration.

## Nicht-Ziele (YAGNI)

- Kein Voll-LLM-Tagging jeder Passage (Ansatz C) im ersten Wurf.
- Keine Ödipus-/Mythen-Bücher in dieser Iteration.
- Kein Umbau des NMDS-Rechenkerns (tfidf/nmds/curate_edges bleiben unverändert).
- Keine neue zweite Content-Collection — die bestehende `themen`-Collection wird um
  eine `theme`-Dimension erweitert.

## Architektur

Zwei getrennt testbare Teile.

### Teil A — Daten-Pipeline (Bischof-Inhalt → Layout)

Spiegelt die Hypnosystemik-Pipeline; neu ist nur der Kopf (PDF→Konzept→Passage).

1. **PDF-Extraktion.** `pdftotext` zieht beide Bücher inkl. hierarchischer Nummerierung
   nach `Bibliothek/Allgemeine Psychologie Materials/_extracted/` (gitignored).
2. **Konzept-Knoten (hybrid).** LLM-Pass über den Rohtext schlägt Bischofs benannte
   Konzepte + Cluster-Zuordnung vor; der Nutzer redigiert zur Endliste → neues
   `scripts/nmds-layout/manifest_bischof.py` (Format wie `manifest.py`:
   `slug, cluster, title`, ~40–60 Einträge, ~4–6 Cluster).
3. **Passagen-Retrieval.** Pro kuratiertem Konzept die relevanten Buchstellen einsammeln
   (TF-IDF/Keyword-Retrieval der Konzept-Begriffe über beide Bücher, `tfidf.py`
   wiederverwendet; optional LLM-verdichtet). Ergebnis: je Knoten ein Ordner
   `Bibliothek/Allgemeine Psychologie/<nr>-<slug>/` mit
   `quelle.md` (Corpus, lokal), `meta.json` (`title`, `summary`, `status`),
   optional `text.md` (eigener Fließtext).
4. **NMDS-Layout.** Bestehende Region-per-Cluster-Logik (`build_layout.py` + `nmds.py`),
   auf Bischof-Manifest/-Verzeichnis parametrisiert → `out/layout.bischof.json`.
5. **Kanten.** `curate_edges.py` unverändert → `out/edges.curated.bischof.json`.
6. **Content-Gen.** `sync_content.py` (thema-parametrisiert) schreibt
   `site/src/content/themen/<slug>/index.md` mit Frontmatter inkl.
   `theme: allgemeine-psychologie`.

**Parametrisierung statt Duplikat:** `extract_corpus.py`, `build_layout.py`,
`sync_content.py` erhalten das Thema (Manifest-Modul + `Bibliothek`-Unterordner) als
Argument, sodass **beide** Themen dieselben Skripte nutzen. `tfidf.py`, `nmds.py`,
`curate_edges.py` bleiben unangetastet.

### Teil B — Site-Generalisierung (Single- → Multi-Map)

> **Nachtrag 2026-07-30 (bei der Planung entdeckt):** Diese Generalisierung ist im
> Codebase bereits weitgehend **umgesetzt**. `scripts/nmds-layout/spaces.py`
> abstrahiert Räume über die Env `SPACE`; ein zweiter Raum „herausforderungen"
> existiert komplett (Schema-Factory `themaSchema` in `content.config.ts`,
> `HERAUS_CLUSTER_META` + `buildGraph(collection, clusters)` in `graph.ts`, eigene
> Seiten, `rebuild.sh [raum]`). Für Psyche bleibt daher nur, den **dritten Raum
> `psyche` nach diesem Muster** zu ergänzen (Details im Implementierungsplan
> `docs/superpowers/plans/2026-07-30-psyche-bischof-konzeptkarte.md`). Der einzige
> echte neue Code-Teil ist ein Regionen-Grid für 5 Cluster (bislang nur 4 Quadranten).

Minimal-invasiv; Hypnosystemik läuft unverändert weiter.

- **Schema** (`content.config.ts`): Feld `theme: z.enum(['hypnosystemik',
  'allgemeine-psychologie'])`. Cluster-Enum + `CLUSTER_META` pro Thema (Bischof-Cluster
  mit eigenen Labels/Farben statt k1–k4).
- **Graph-Lib** (`graph.ts`): `buildGraph(theme)` filtert die `themen`-Collection nach
  Thema; `CLUSTER_META` themabezogen auflösen.
- **Layout** (`build_layout.py`): Region-Grid von fix-4-Quadranten auf N-Cluster
  verallgemeinern (Grid nach Cluster-Anzahl).
- **Seite:** neue `site/src/pages/psyche/index.astro` (Klon von `erleben/index.astro`)
  rendert `buildGraph('allgemeine-psychologie')` via `GraphKonstellation`.
  `[teil].astro` filtert künftig `psyche` **und** `erleben` heraus (beide bespoke).
- Bestehende Hypnosystemik-Einträge erhalten rückwirkend `theme: hypnosystemik`
  (via `sync_content.py`), damit `buildGraph('hypnosystemik')` sie findet.

## Datenfluss

```
PDF (2) --pdftotext--> _extracted/*.txt
   --LLM+Kuration--> manifest_bischof.py (Knoten+Cluster)
   --Retrieval--> Bibliothek/Allgemeine Psychologie/<nr>-<slug>/{quelle.md,meta.json}
   --build_layout(thema=ap)--> out/layout.bischof.json + edges.suggested
   --curate_edges--> out/edges.curated.bischof.json
   --sync_content(thema=ap)--> site/src/content/themen/<slug>/index.md (theme: allgemeine-psychologie)
   --buildGraph('allgemeine-psychologie')--> /psyche  (GraphKonstellation)
```

## Urheberrecht / Datenhaltung

- `Bibliothek/*` ist gitignored → PDFs, `_extracted/` und die `quelle.md`-Rohpassagen
  bleiben **lokal** und gehen NICHT nach GitHub/Netlify.
- Öffentlich (committet in `site/src/content/`) gehen **nur eigene Zusammenfassungen**
  (`meta.json.summary`, optional `text.md`) — **keine** verbatim übernommenen,
  urheberrechtlich geschützten Buchpassagen. `quelle.md` dient ausschließlich der
  TF-IDF-Positionsberechnung und wird nicht veröffentlicht.

## Validierung / Qualitätsmaß

- **NMDS-Stress** wird geloggt (wie bei Hypnosystemik). Richtwert < ~0.2 als
  Kohärenz-Indikator; darüber Konzept-/Retrieval-Revision.
- **Build-Gate:** `cd site && npm run build` + bestehende vitest-Tests grün — die
  Hypnosystemik-Karte darf nicht brechen (Regression-Schutz).
- **Reality-Check:** nach Schritt A4 (Layout steht) visuelle/inhaltliche Sichtprüfung,
  BEVOR der Site-Umbau (Teil B) beginnt.

## Kosten-Realität

Aufwand ist **linear**, nicht exponentiell. Der Rechenkern (NMDS ~O(k²) in der
Knotenzahl, TF-IDF ~linear zum Text) ist bei ~50 Knoten trivial und praktisch
unabhängig von der Buchzahl. Dominant ist die einmalige Konzept-Extraktion +
Passagen-Retrieval (Schritte A2–A3), linear zur Textmenge. Ödipus/Mythen später =
mehr Passagen pro Knoten, kein Neuentwurf.

## Phasenschnitt (empfohlene Reihenfolge)

1. **Teil A bis A4** → `layout.bischof.json` steht, Stress geprüft, Reality-Check.
2. **Teil B** Site-Generalisierung (Schema, graph.ts, build_layout-Regionen,
   psyche-Seite, Hypnosystemik-`theme`-Backfill).
3. **Teil A6** Content-Gen + Build-Gate + Deploy.

## Entschiedene Detailfragen

- **Retrieval-Granularität:** Kapitel-Chunks als Retrieval-Einheit (die Kapitel/
  Unterkapitel der hierarchischen Nummerierung, nicht Einzelabsätze).
- **Cluster-Farbpalette:** wie vorgeschlagen (~4–6 thematische Cluster, eigene
  Labels/Farben aus `reference/design-tokens.md`), Feinschliff bei der Kuration.
- **`/psyche`-Einleitungstext:** keiner — die Seite trägt nur die Konstellation
  (wie `/erleben`).
