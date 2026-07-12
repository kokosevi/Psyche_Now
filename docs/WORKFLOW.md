# Workflow: Psyche_Now Homepage

Dieses Dokument beschreibt den kompletten Weg von der Idee bis zur veröffentlichten
Seite — und vor allem: **wann du in Claude Design arbeitest, wann in Claude Code**,
und wie der Hand-off dazwischen sauber funktioniert.

---

## Überblick: Die Werkzeugkette

```
 Inhalt sammeln     Design            Hand-off          Code            Veröffentlichen
 ─────────────      ──────────        ────────          ────            ───────────────
 Bibliothek/    →   Claude Design  →  design/HANDOFF →  Claude Code  →  GitHub → Netlify
 content/           (claude.ai)       + Artifact-Code   (dieser Ordner)          + Umami
```

| Werkzeug        | Wofür                                          | Wo                     |
|-----------------|------------------------------------------------|------------------------|
| Claude Design   | Aussehen & Gefühl, Layout, Screens als Mockup  | claude.ai (Browser)    |
| Claude Code     | Echter Code, Struktur, Interaktivität, Deploy  | dieser Ordner          |
| GitHub          | Versionsverwaltung, Quelle für Deploy          | github.com             |
| Netlify         | Hosting, Auto-Deploy bei jedem Push            | netlify.com            |
| Umami           | Datenschutzfreundliche Reichweiten-Statistik   | Umami Cloud / self-host|

---

## Faustregel: Design vs. Code

> **Aussehen & Gefühl → Claude Design.
> Echtheit, Daten, Struktur, Deploy → Claude Code.**

| Du arbeitest in **Claude Design**, wenn du…      | Du arbeitest in **Claude Code**, wenn du…            |
|--------------------------------------------------|------------------------------------------------------|
| ein Layout / eine Seite visuell entwerfen willst | das Astro-Projekt aufsetzt oder umbaust              |
| Farben, Schriften, Abstände ausprobierst         | ein Mockup in echten, wartbaren Code überführst      |
| einen Screen als klickbares Mockup zeigen willst | interaktive Logik verdrahtest (Graph, Quiz, Filter)  |
| Text-Tonalität / Copy testest                    | Inhalte aus `Bibliothek/` in Markdown pflegst        |
| schnell iterieren willst, ohne etwas zu bauen    | Git, Netlify-Deploy, Umami, Performance, Barrierefr. |

**Merksatz für den Zweifelsfall:** Wenn du es *anschauen* willst → Design.
Wenn es *funktionieren* oder *deployt* werden soll → Code.

---

## Ordnerstruktur

```
Psyche_Now/                    ← Git-Repo-Wurzel
├── site/                      ← Das Astro-Projekt (wird beim Scaffold angelegt)
│   └── src/content/themen/    ← Deine Inhalte: 1 Markdown = 1 Thema = 1 Graph-Knoten
├── content/drafts/            ← Roh-Notizen & Entwürfe, bevor sie zu Themen werden
├── Bibliothek/                ← Inhaltliche Quellen (PDFs, Slides) — Kontext, kein Website-Text
├── design/                    ← Hand-off aus Claude Design
│   ├── artifacts/             ← exportierter HTML/React-Code aus Artifacts
│   ├── screenshots/           ← Screenshots der Designs
│   └── HANDOFF.md             ← Hand-off-Protokoll (was, wohin, wie interaktiv)
├── reference/                 ← Design-Tokens, Brand, sonstige Referenzen
│   └── design-tokens.md       ← Farben/Fonts/Abstände — gemeinsame Sprache Design↔Code
├── docs/WORKFLOW.md           ← dieses Dokument
├── netlify.toml               ← Netlify-Build-Konfiguration
└── README.md
```

---

## Die zwei Verträge, die den Hand-off sauber machen

Ein sauberer Hand-off steht und fällt mit zwei Dingen, auf die sich Design und Code
verlassen:

1. **Gemeinsame Design-Tokens** (`reference/design-tokens.md`)
   Farben, Schriften und Abstände sind *einmal* definiert. In Claude Design nennst du
   sie beim Namen ("Hintergrund = `--color-bg`, Überschrift = Schrift `Serif`"), im Code
   sind exakt dieselben Werte hinterlegt. So sieht das Endergebnis aus wie das Mockup.

2. **Das Hand-off-Protokoll** (`design/HANDOFF.md`)
   Pro Design hältst du kurz fest: *Welcher Screen? Auf welche Seite gehört er? Was ist
   interaktiv? Woher kommt der Inhalt? Was ist echt, was Platzhalter?* Template und
   Beispiel liegen in der Datei.

Der Hand-off läuft in **zwei Richtungen**:

- **Code → Design:** `reference/DESIGN-BRIEF.md` bringt Claude Design auf den aktuellen
  Stand (Design-System, was schon existiert, Grenzen, Aufgabe). Diese Datei kommt **einmal**
  ins Claude.ai-**Projektwissen** und gilt dann für jede Session automatisch — nicht jedes
  Mal neu einfügen. Bei Änderungen am Design-System aktualisieren und im Projektwissen ersetzen.
- **Design → Code:** Claude Design liefert ein **selbst-enthaltendes Bündel** (HTML/CSS,
  `bilder/`, `fonts/`, plus eigenes `HANDOFF.md`). Ablage: **ein Ordner pro Hand-off** unter
  **`design/handoffs/<JJJJ-MM-TT>-<kurzname>/`** (Beispiel:
  `design/handoffs/2026-07-12-erleben-gestalten/`). Danach in Claude Code sagen:
  *„Setze den Hand-off in `design/handoffs/<…>` um."* Ich kopiere Assets nach `site/public/`
  und überführe HTML/CSS in Astro.

---

## Schritt für Schritt

### Phase 0 — Einmalig: Setup (erledigen wir in Claude Code)

1. Astro-Projekt scaffolden (`site/`) mit Content Collections + Beispiel-Thema + Graph-Prototyp.
2. Design-Tokens aus `reference/design-tokens.md` ins Projekt übernehmen.
3. Git-Repo mit GitHub verbinden.
4. Netlify mit dem GitHub-Repo verbinden (Auto-Deploy).
5. Umami-Konto anlegen und Tracking-Snippet einbauen.

> Status: **Schritte 1–5 erledigt + erster Design-Hand-off umgesetzt.**
> Live: https://psychenow.netlify.app · Repo: https://github.com/kokosevi/Psyche_Now
> (public, `main`, Auto-Deploy). Umami aktiv (bei gesetzten `PUBLIC_UMAMI_*`).
> Aktuelles Design: **«Erleben gestalten»** (4 Seiten: Landing + Psyche/Herausforderungen/
> Erleben) aus `design/handoffs/2026-07-12-erleben-gestalten/`. Das frühere «Kraftfeld»-
> Scaffold wurde ersetzt (in der Git-Historie erhalten).

### Phase 1 — Inhalt vorbereiten (du)

- Quellmaterial liegt in `Bibliothek/` (PDFs, Slides — nur Kontext, kommt nicht 1:1 auf die Seite).
- Rohgedanken/Entwürfe schreibst du in `content/drafts/`.
- Ergebnis pro Thema: ein Titel, ein Kerngedanke, verwandte Themen (für den Graph).

### Phase 2 — Design (Claude Design, claude.ai)

- Entwirf den Screen / die Komponente als **Artifact** (HTML oder React).
- Halte dich an die **Design-Tokens** (Farben/Fonts beim Namen nennen).
- Iteriere am Aussehen, bis es sitzt.
- **Exportiere** am Ende: den Artifact-Code + einen Screenshot.

### Phase 3 — Hand-off (die Brücke)

1. Artifact-Code speichern → `design/artifacts/<screen-name>/`
2. Screenshot speichern → `design/screenshots/<screen-name>.png`
3. Neuen Eintrag in `design/HANDOFF.md` ausfüllen (Template in der Datei).
4. In Claude Code sagen: *"Bitte Hand-off `<screen-name>` umsetzen."*

### Phase 4 — Code (Claude Code, dieser Ordner)

- Ich überführe das Mockup in echten Astro-Code (Layouts, Komponenten, Content).
- Interaktive Elemente werden als **Islands** gebaut:
  - **Selbsttests/Quizze** — lokaler State, keine Speicherung, keine Registrierung.
  - **Scroll-Storytelling** — Inhalte entfalten sich beim Scrollen.
  - **Interaktive Diagramme** — z. B. das hypnosystemische Modell zum Anklicken.
  - **Filter/Suche** — über alle Themen.
  - **Graph-View (Karpathy-Idee)** — Knoten = Themen, Kanten = `related`-Verlinkungen
    aus dem Markdown-Frontmatter. Klick auf einen Knoten → zur Themenseite.
- Lokal testen: `cd site && npm run dev`.

### Phase 5 — GitHub

```bash
git add -A
git commit -m "Beschreibung der Änderung"
git push
```

### Phase 6 — Netlify + Umami (automatisch)

- **Netlify** baut bei jedem Push automatisch neu und veröffentlicht.
- **Umami** zählt Besuche datenschutzfreundlich (kein Cookie-Banner nötig).
- Fertig — die Änderung ist live.

---

## Das verbindende Datenmodell: das Frontmatter

Jede Themen-Datei beginnt mit einem kleinen Kopf (Frontmatter). Ein einziges Feld —
`related` — speist gleichzeitig **drei** interaktive Features:

```markdown
---
title: "Hypnosystemik"
summary: "Kurzer Kerngedanke in 1–2 Sätzen."
tags: ["Therapie", "Systemik"]
related: ["allgemeine-psychologie", "mythos-und-psyche"]
---

Hier steht der eigentliche Inhalt des Themas …
```

- `related` → **Kanten im Graph** und **"verwandte Themen"-Links** auf der Seite.
- `tags` → **Filter/Suche**.
- `title` / `summary` → **Knoten-Beschriftung** und **Vorschau-Karten**.

Ein Datenmodell, mehrere Features — deshalb bleibt die Seite pflegeleicht.

---

## Was NICHT gebraucht wird (bewusste Grenzen)

- Keine Registrierung, keine Nutzerkonten.
- Keine Zahlungsfunktion.
- Keine Datenbank — alle Inhalte leben als Markdown im Repo.
- Quiz-Ergebnisse bleiben im Browser (kein Server, keine Speicherung).
```
