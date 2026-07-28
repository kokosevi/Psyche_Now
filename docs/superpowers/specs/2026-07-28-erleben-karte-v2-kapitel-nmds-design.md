# Design: „Erleben"-Karte v2 — Kapitel-Cluster mit NMDS-Layout

**Datum:** 2026-07-28
**Seite:** `/erleben` (Varianten **Konstellation** + **Hybrid**; Force-Graph bleibt unangetastet)
**Quelle des Inhalts:** Google Doc „Hypnosystemische Therapie & Beratung" (ID
`10pzMPStc5Zh57O5mfcfup2jMiFYIJ1mwL3AEn3eOFx4`), identisch mit `Bibliothek/Hypnosystemik/`.
⚠️ Urheberrechtlich geschützt — nur eigene Zusammenfassungen publizieren, Transkripte bleiben
gitignored. Aus den Transkripten wird **nur** das NMDS-Layout (x/y-Koordinaten) abgeleitet.

## 1. Ausgangslage & Ziel

Der erste Bau (`2026-07-24-erleben-second-brain-design.md`) hat ~30 Konzept-Knoten in **fünf
thematischen** Clustern (grundlagen/symptom/anwendung/prozess/selbst) mit **handplatzierten**
x/y-Koordinaten. Diese v2 stellt die Karte auf die **Kapitelstruktur des Dokuments** um:

- **Jedes Unterkapitel ist ein Knoten** (Konzept-Ebene; Meta-Intros und reine Sitzungs-
  Transkripte werden nicht zu Knoten).
- **Vier Cluster = Kapitel 1–4** (Kapitel 5 „Schlusswort" wird ignoriert). Cluster sind
  räumlich getrennte „Inseln" — wie die Gruppierungen auf der Klenico-„Depression"-Karte.
- **Räumliche Distanz ist nur INNERHALB eines Clusters bedeutungstragend.** Sie wird per
  **NMDS** (nicht-metrische multidimensionale Skalierung) aus einem inhaltlichen Kriterium
  berechnet (siehe §4).
- **Cluster-übergreifende Kanten** verbinden inhaltlich verwandte Unterkapitel.

Betrifft **Konstellation** und **Hybrid** (beide konsumieren dasselbe `buildGraph()`);
**Force-Graph** wird nicht gepflegt, rendert die neuen Daten aber weiter fehlerfrei.

## 2. Kapitelstruktur des Dokuments (Ist)

| Kap. | Titel | Ebene der Knoten |
|---|---|---|
| 1 | Grundlagen | 1.3–1.17 (1.2 Kursüberblick = Meta → kein Knoten) |
| 2 | Hypnosystemischer Blick auf Herausforderungen | 2.1–2.10 |
| 3 | Handwerk | 3.1.2–3.1.12 (10 Prozessschritte; 3.1.1 Intro raus), 3.2 Fallanalyse, 3.3.2–3.3.6 (3.3.1 Intro raus) |
| 4 | Praxisfälle | 4.2–4.9 (je 1 Knoten pro Fall; Inhalt = jeweiliger „Überblick", nicht die Sitzungen) |
| 5 | Schlusswort | ignoriert |

## 3. Knoten-Set (Konzept-Ebene, 50 Knoten)

Bestehende Dateien in `site/src/content/themen/` werden **weiterverwendet und neu einem
Kapitel-Cluster zugeordnet** (nur `cluster` + `x/y` + `related` ändern sich); ~20 neue Knoten
kommen dazu (vorerst als **Stubs**: Titel + Summary + „Inhalt folgt").

### K1 — Grundlagen (15)
Bestehend: `erleben-erzeugen` (1.9), `hirnforschung` (1.10), `grundlagenmodell` (1.11),
`netzwerk-modell` (1.12/1.13), `trance-transparenz` (1.14), `selbsterfahrung` (1.15),
`probleme-basteln` (1.16), `potenzialhypothese` (1.17), `hypnosystemischer-ansatz` (1.7),
`angst` (1.8 Praxisbeispiel Angst).
Neu: `sag-mal-gunther` (1.3), `werdegang-wurzeln` (1.3b), `hypnosyst-denken` (1.4),
`rollenverstaendnis` (1.5), `haltung` (1.6).

### K2 — Herausforderungen (10, alle bestehend)
`ursachen` (2.1), `symptomverstaendnis` (2.2), `neutralitaet` (2.3), `abgrenzung` (2.4),
`diagnosen` (2.5), `burnout` (2.6), `entscheidungen` (2.7), `restriktionen` (2.8),
`versoehnung` (2.9), `loesung-aller-probleme` (2.10).

### K3 — Handwerk (17)
Bestehend: `beratungssystem` (3.1.2), `auftragsklaerung` (3.1.4), `unterschiede` (3.1.5),
`utilisation` (3.1.6), `steuerposition` (3.1.7), `interventionen` (3.1.8),
`selbstfuersorge` (3.3.2), `eigene-wahrgebung` (3.3.3), `zugang-kompetenzen` (3.3.4),
`innere-weisheit` (3.3.6).
Neu: `zuweisungsdynamik` (3.1.3), `utilisation-problemsituationen` (3.1.9),
`utilisation-ambivalenzen` (3.1.10), `utilisation-rueckfaelle` (3.1.11),
`abschluss-transfer` (3.1.12), `fallanalyse-ungewisses` (3.2),
`imagination-steuerposition` (3.3.5).

### K4 — Praxisfälle (8, alle neu; Inhalt aus dem jeweiligen „Überblick")
`depression` (4.2), `trauer-schuld` (4.3), `schmerzen` (4.4), `panik` (4.5),
`paarkonflikt` (4.6), `trauma` (4.7), `sucht` (4.8), `essverhalten` (4.9).

Jede der 30 bestehenden Dateien bildet genau auf ein Kapitel ab (keine Waisen). Das alte
5-Cluster-Schema entfällt vollständig.

## 4. NMDS-Layout (offline, einmalig, gebacken)

Ein eigenständiges Skript unter `scripts/nmds-layout/` (nicht Teil des Astro-Builds,
dependency-frei außer `numpy`). Ablauf:

1. **Korpus bauen.** Das Doc wird in Knoten-Texte zerlegt (Split an den Unterkapitel-
   Überschriften). Für K4 = Text des „Überblick"-Abschnitts je Fall. Ergebnis liegt lokal
   unter `Bibliothek/` bzw. `scripts/nmds-layout/corpus/` (gitignored).
2. **Vektorisieren (TF-IDF).** Tokenisierung (lowercase, deutsche Stoppwortliste, Timestamps
   `(mm:ss)` und Füllwörter entfernt), Term-Frequency × log-inverse-Document-Frequency über
   den gesamten Korpus. Selbst implementiert (numpy), keine sklearn-Abhängigkeit.
3. **Dissimilarität je Cluster.** Innerhalb jedes Clusters: `d(i,j) = 1 − cos(v_i, v_j)`.
   → symmetrische Distanzmatrix pro Cluster.
4. **NMDS pro Cluster.** Nicht-metrische MDS auf die **Rangordnung** der Dissimilaritäten
   (isotone Regression + SMACOF-Stress-Majorisierung), Ziel 2D. Mehrere Inits mit **festem
   Seed**, niedrigster Stress gewinnt → deterministisch reproduzierbar.
5. **Auf die Bühne platzieren.** 100×100-Canvas, 2×2-Anordnung der vier Cluster-Regionen mit
   Puffer dazwischen. Jede Cluster-Wolke wird zentriert, isotrop skaliert und in ihre Region
   gelegt (Aspect-Ratio erhalten, Padding an den Rändern). Räumliche Distanz *zwischen*
   Clustern ist damit bedeutungslos (nur Kapitelzugehörigkeit); *innerhalb* spiegelt sie die
   inhaltliche Nähe.
6. **Kanten-Vorschläge.** Cross-Cluster-Kosinus-Ähnlichkeit über alle Knotenpaare; die
   stärksten Paare (über Schwelle / Top-k) werden als Vorschlagsliste ausgegeben und
   **fachlich kuratiert**. Sinnvolle bestehende `related`-Kanten bleiben erhalten.
7. **Output.** `scripts/nmds-layout/out/layout.json` = `{ slug: {cluster, x, y}, edges: [...] }`.
   Ein Writer-Schritt schreibt `cluster`, `x`, `y` ins Frontmatter der Knoten-Dateien und die
   kuratierten `related`-Kanten. Committet werden **nur** Koordinaten/Kanten, nie Transkripte.

**Kriterium in einem Satz:** Zwei Unterkapitel desselben Kapitels liegen umso näher
beieinander, je ähnlicher ihr fachliches Vokabular ist (TF-IDF-Kosinus) — inhaltlich
verwandte Konzepte bilden sichtbare Nachbarschaften innerhalb der Kapitel-Insel.

## 5. Datenmodell-Änderungen

`site/src/content.config.ts`:
```ts
export const CLUSTERS = ['k1', 'k2', 'k3', 'k4'] as const;
```
`lektion?: number` bleibt optional (jetzt als Kapitel-Referenz nutzbar, z. B. `1.9`).
`site/src/lib/graph.ts` — `Cluster`-Typ + `CLUSTER_META`:

| id | label | colorVar |
|---|---|---|
| `k1` | Grundlagen | `--ink` |
| `k2` | Herausforderungen | `--marker` |
| `k3` | Handwerk | `--ink-2` |
| `k4` | Praxisfälle | `--sun-deep` |

`assembleGraph`/`buildGraph`-Logik bleibt unverändert (Kanten aus `related`, Integritätsregel,
Dedup). Nur Enum-Werte und Metadaten wechseln.

## 6. Rendering (nur Konstellation-Komponente)

`GraphKonstellation.astro` bekommt zusätzlich zu den bestehenden Knoten/Kanten:
- **Cluster-Hull/Region:** pro Cluster ein dezent getönter, abgerundeter Hintergrund-Bereich
  (Bounding-Box der Cluster-Knoten + Padding) in der Cluster-Farbe (sehr niedrige Deckkraft),
  damit die vier Inseln wie auf der Klenico-Karte sofort lesbar sind.
- **Cluster-Titel** (Amatic SC) an der Region.
- Bestehende Interaktion (Hover/Fokus hebt Knoten, färbt Kanten gold) bleibt.
Hybrid erbt das automatisch (nutzt dieselbe Komponente) inkl. Drift/Highlight.
**Force-Graph wird nicht angefasst.**

## 7. Verifikation

- `site/src/lib/graph.test.ts` erweitern: Cluster-Enum = {k1,k2,k3,k4}; jeder Knoten in genau
  einem Cluster; keine baumelnden `related`-Slugs; `x/y ∈ [0,100]`; jede der vier Kapitel-IDs
  hat ≥1 Knoten.
- NMDS-Skript: eigener Determinismus-Test (fester Seed → bit-identische Koordinaten bei
  zwei Läufen) + Stress-Wert wird geloggt.
- `npm run build` erzeugt `/erleben`, Konstellation, Hybrid und je eine `thema`-Seite pro
  Knoten fehlerfrei; `astro check` grün.
- Manuell: vier räumlich getrennte Cluster sichtbar; Cross-Cluster-Kanten vorhanden;
  Klick auf Knoten → richtige Unterseite; reduced-motion stoppt Drift.

## 8. Dateien (neu/geändert)

**Neu:**
`scripts/nmds-layout/` (Korpus-Extraktor, TF-IDF+NMDS, Frontmatter-Writer, Determinismus-Test) ·
`site/src/content/themen/*.md` (~20 neue Knoten, Stubs) ·
`site/src/content/themen/depression.md` … (K4, aus „Überblick").

**Geändert:**
`site/src/content.config.ts` (CLUSTERS = k1..k4) ·
`site/src/lib/graph.ts` (`Cluster`-Typ + `CLUSTER_META`) ·
alle 30 bestehenden `themen/*.md` (Frontmatter: `cluster`, `x`, `y`, tw. `related`) ·
`site/src/components/graph/GraphKonstellation.astro` (Cluster-Hulls + Labels) ·
`site/src/lib/graph.test.ts`.

**Unangetastet:** `GraphForce.astro`, `hybrid.astro`, `konstellation.astro`,
`VariantSwitcher.astro`, `thema/[slug].astro`.

## 9. Nicht in diesem Bau

- Volltexte der neuen K1/K3-Knoten (bleiben Stubs) und ausformulierte K4-Falltexte über die
  Kurz-Zusammenfassung hinaus.
- Finale Variantenauswahl / Entfernen von Force-Graph.
- Upgrade des NMDS-Kriteriums auf Embeddings (später optional möglich, gleiche Pipeline-Stufe).
