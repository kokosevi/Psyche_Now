# K4-Fall-Subpages aus den Life-Lessons-Transkripten

**Datum:** 2026-07-28
**Ziel:** Für die 8 Praxisfall-Knoten (Cluster k4) je eine ausformulierte Subpage
erzeugen, auf Basis der Kapitel-Transkripte aus
`Bibliothek/Hypnosystemik/Life Lessons - Transkripte.txt`.

## Umfang

Betroffene Knoten / Dateien (`site/src/content/themen/<slug>.md`):

| slug | Titel | Kapitel | Content-Zeilen (Transkript) |
|------|-------|---------|------------------------------|
| depression   | Depressionen                 | 4.2 | Sitzungen 476, 483 · Komm. 490 · Überblick 497 |
| trauer-schuld | Trauer & Schuld              | 4.3 | Sitzung 509 · Komm. 516 · Überblick 523 |
| schmerzen     | Chronische Schmerzen         | 4.4 | Sitzungen 535, 542 · Komm. 549 · Überblick 556 |
| panik         | Panikattacken                | 4.5 | Sitzungen 568, 575 · Komm. 582 · Überblick 589 |
| paarkonflikt  | Paarkonflikt                 | 4.6 | Sitzung 601 · Komm. 608 · Überblick 615 |
| trauma        | Trauma                       | 4.7 | Sitzungen 627, 634 · Komm. 641 · Überblick 648 |
| sucht         | Alkohol- und Nikotinsucht    | 4.8 | Sitzungen 660, 667 · Komm. 674 · Überblick 681 |
| essverhalten  | Ess- und Bewegungsgewohnheiten | 4.9 | Sitzung 693 · Komm. 700 (kein eigener Überblick) |

## Was sich pro Datei ändert

- Body `Inhalt folgt.` → ausformuliertes Fallporträt (siehe Vorlage).
- `status: stub` → `status: full`.
- Alle anderen Frontmatter-Felder (title, cluster, summary, related, x, y) bleiben
  **unverändert** — Kartenpositionen und Kanten werden nicht berührt.

## Seiten-Vorlage

Erklärende Fachprosa, dritte Person, Deutsch, ~400–600 Wörter, kein H1 im Body
(Titel + Cluster-Label rendert die Seite bereits). Vier feste Abschnitte:

```markdown
## Das Anliegen
Womit kommt die Person / das Paar? Symptom, Auftrag, Ausgangslage.

## Der hypnosystemische Blick
Wie das Symptom umgedeutet wird — als unwillkürlich erzeugter, sinnhafter
Prozess statt Defizit; welche innere Logik sichtbar wird.

## Im Prozess
Zentrale Interventionen/Bewegungen aus den Sitzungen (Utilisation,
Steuerposition, Ambivalenz-/Seitenarbeit, Ressourcen …), fallspezifisch.

## Was bleibt
Kernbotschaft des Falls — die übertragbare „Life Lesson".
```

## Constraints

- **Keine Eigennamen** aus den Transkripten (z. B. „Herr Sundater", „Frau Sommer").
  Neutral formulieren: „der Klient", „die Klientin", „das Paar".
- Keine erfundenen Fakten — nur, was das Kapitel hergibt.
- Ton konsistent mit den vorhandenen `summary`-Feldern.

## Ausführung

Ein Subagent pro Kapitel (8 parallel). Jeder liest gezielt seine Content-Zeilen
(Überblick + Kommentierung zuerst — am dichtesten; Sitzungen für konkrete
Prozessdetails), schreibt genau eine `.md`. Danach: Stichprobe gegenlesen,
`astro build` + Vitest.

## Verifikation

- `npm run build` (Astro) fehlerfrei; alle 8 Dateien `status: full`, kein
  „Inhalt folgt." mehr.
- `npx vitest run` grün (Schema/Graph unverändert).
- Stichprobe: 1–2 Seiten auf Länge, Ton, keine Eigennamen prüfen.
