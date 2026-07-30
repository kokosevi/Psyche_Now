# Design: NMDS-Karte „Herausforderungen: Woran Glück scheitert"

Datum: 2026-07-30 · Teil 2 der Homepage (`/herausforderungen`)

## Ziel

Eine NMDS-Karte der relevanten Herausforderungen, die „Glück" für Menschen heute
schwierig machen — analog zur bestehenden „Erleben"-Karte (`/erleben`), aber als
eigener, unabhängiger Raum. Jede Herausforderung ist ein Knoten; die 2D-Lage
entsteht aus einer Distanzmatrix per Non-metric Multidimensional Scaling (NMDS).

## Entscheidungen (im Brainstorming festgelegt)

- **Quelle der Herausforderungen: Hybrid** — Basis aus dem vorhandenen
  Gunther-Schmidt/Hypnosystemik-Korpus (dort benannte Fallen/Konflikte/Sinnkrisen),
  erweitert um aktuelle Glücks-/Wohlbefindensforschung. Der User kuratiert final.
- **Distanz-Input: text-basiert (wie Erleben)** — jede Herausforderung bekommt einen
  reichen Steckbrief-Text; Distanz = TF-IDF-Cosinus über die bestehende Pipeline.
  Embedding-Cosinus als Ein-Zeilen-Upgrade, falls die Karte zu wortgetrieben wirkt.
- **Reihenfolge:** Ich baue eine vollständige Erstfassung end-to-end (Sammeln →
  Steckbriefe → Karte → Seite). **Der User kuratiert die Knoten danach**, indem er
  die Ordner unter `Bibliothek/Herausforderungen/` editiert und `rebuild.sh` erneut
  laufen lässt.
- **YAGNI:** kein neues Distanzverfahren, keine Hierarchie/Unter-Unter-Cluster —
  flache Karte wie Erleben, ~4 Cluster in 4 Quadranten-Regionen.

## Architektur — zwei Räume statt einer

Erleben und Herausforderungen sollen koexistieren, ohne dass Erleben sich ändert.
Das bestehende Tooling ist an drei Stellen fest auf Hypnosystemik verdrahtet; diese
werden auf einen `SPACE`-Begriff verallgemeinert (Default = Erleben, byte-identisch).

### Pipeline (`scripts/nmds-layout/`)

- Neues Modul `spaces.py`: Konfiguration je Raum
  - `erleben`: BIB=`Bibliothek/Hypnosystemik`, NODES=bisherige Liste, Cluster
    k1–k4 + Regionen, THEMEN=`site/src/content/themen`.
  - `herausforderungen`: BIB=`Bibliothek/Herausforderungen`, NODES=neue Liste,
    Cluster h1–h4 + Regionen, THEMEN=`site/src/content/herausforderungen`.
- `manifest.py`, `build_layout.py`, `curate_edges.py`, `sync_content.py`,
  `extract_corpus.py` lesen die aktive Space-Config (per Env-Var `SPACE`, Default
  `erleben`). Ohne `SPACE` bleibt das Erleben-Verhalten unverändert (Determinismus,
  seed=42).
- `rebuild.sh` nimmt den Space-Namen als Argument: `rebuild.sh herausforderungen`.
- Knoten-Ordnerschema wie Erleben: `<seq>-<slug>/` mit `quelle.md` (Belege/Notizen,
  bleibt lokal, geht nie live), `text.md` (veröffentlichbarer Steckbrief = TF-IDF-
  Input), `meta.json` (`title`, `summary`, `status`).

### Site (`site/`)

- Zweite Content-Collection `herausforderungen` in `content.config.ts`, gleiches
  Schema wie `themen`, aber eigener Cluster-Enum (`h1`–`h4`).
- `lib/graph.ts` verallgemeinern: `buildGraph` bekommt Collection-Name + ClusterMeta
  als Parameter; Cluster-Typ wird generisch (string). Dünner Erleben-Wrapper bleibt.
- `GraphKonstellation.astro`: statt `CLUSTER_META`-Import die Cluster aus
  `graph.clusters` lesen; neue Props `basePath` (Thema-Link) und `ariaLabel`. Erleben
  ruft mit seinen Werten auf → unverändert.
- Neue Seiten:
  - `pages/herausforderungen/index.astro` — die Karte.
  - `pages/herausforderungen/thema/[slug].astro` — Knoten-Subpages (Spiegel von
    `erleben/thema/[slug].astro`).
- `pages/[teil].astro`: `herausforderungen` aus `getStaticPaths` ausschließen (wie
  `erleben` schon), sonst Routen-Kollision mit `index.astro`.

## Ablauf (Phasen)

1. **Longlist** — zwei Recherche-Agenten parallel: (a) Extraktion aus dem
   Schmidt-Korpus mit Belegen, (b) Glücksforschung mit Quellen.
2. **Shortlist** — verdichten auf ~20–30 abgrenzbare Herausforderungen, provisorisch
   auf 4 Cluster verteilt. (User kuratiert später final.)
3. **Knotenordner + Steckbriefe** — pro Herausforderung Ordner + `text.md`
   (eigenständiger Text, kein Verbatim-Transkript) + `meta.json`.
4. **Karte rechnen** — `rebuild.sh herausforderungen` (build_layout → curate_edges →
   sync_content), deterministisch.
5. **Seite bauen** — Astro-Seiten, `npm run build`, verifizieren.

## Nicht-Ziele

- Keine Änderung an der Erleben-Karte oder ihren Inhalten.
- Kein finales Kuratieren der Knoten — das macht der User in einem zweiten Schritt.
- Kein neues Design-System; bestehende Tokens/Komponenten werden wiederverwendet.

## Abnahme

- `/herausforderungen` zeigt eine lesbare Konstellation aus ~20–30 Knoten in
  Cluster-Regionen; Hover hebt Teilgraph hervor (wie Erleben).
- Jeder Knoten verlinkt auf `/herausforderungen/thema/<slug>` mit Steckbrief-Text.
- `npm run build` läuft fehlerfrei; Erleben-Karte unverändert.
- `rebuild.sh herausforderungen` ist idempotent; erneuter Lauf nach Ordner-Edits
  aktualisiert Karte + Content.
