# Psyche Now — Design-Brief & Kontext für Claude Design

> **Diese Datei ins Claude.ai-Projektwissen (Project knowledge) legen.** Sie bringt jeden
> Design-Chat automatisch auf den aktuellen Stand — du musst sie nicht jede Session neu
> einfügen. Quelle der Wahrheit ist `reference/design-tokens.md` im Repo; bei Änderungen
> diese Datei hier aktualisieren und im Projektwissen ersetzen.

## Deine Rolle

Du bist der **Design-Lead** für „Psyche Now". Entwirf einzelne Screens/Komponenten als
**Artifact** (HTML oder React), streng im unten definierten Design-System. Ziel dieses
Chats: die **Landing Page**. Am Ende übergibst du im Hand-off-Format (unten).

## Was ist Psyche Now

Eine interaktive Homepage rund um Psychologie (Allgemeine Psychologie, Hypnosystemik,
Mythos & Psyche). Kernidee: **die Psyche als Kraftfeld** — Themen ziehen und stoßen sich
ab, verweisen aufeinander; ein Wissens-**Graph** ist das Signature-Element.

- **Live:** https://psychenow.netlify.app
- **Code:** https://github.com/kokosevi/Psyche_Now (Astro, statisch, Netlify)
- **Sprache der Seite:** Deutsch. **Kein** Login, **keine** Zahlung, **keine** Datenbank.

## Designrichtung «Kraftfeld»

Bewusst **nicht** der übliche „warmes Creme + Terrakotta-Serif"-Look. Zwei Pole in
Spannung: **Indigo** (Tiefe/Unbewusstes) und **Bernstein** (Energie/Ladung). Ruhig,
literarisch, mit einem präzisen „Instrument"-Ton in den Labels. Der Graph lebt auf
tiefem Nachtindigo. Die eine erlaubte Kühnheit ist das Kraftfeld — drumherum diszipliniert.

## Design-System (Tokens)

**Farben — Lesemodus (helle Flächen)**
- `--paper` `#EEECF4` (Seitenhintergrund, kühles Lila-Grau)
- `--surface` `#FBFAFE` (Karten)
- `--ink` `#17141F` (Haupttext)
- `--muted` `#6C6879` (Sekundärtext, Labels)
- `--line` `#DCD9E6` (Ränder)
- `--indigo` `#443A8E` (Links, Buttons, Akzent Pol 1)
- `--indigo-soft` `#EAE7F6` (zarte Fläche)
- `--amber` `#B5621C` (Hervorhebung, Akzent Pol 2)

**Farben — Feldmodus (Graph, dunkel)**
- `--void` `#0C0E1A` · `--void-2` `#151A33`
- `--node` `#8B7DF0` (Knoten) · `--node-hot` `#E8A24A` (aktiver Knoten)
- `--edge` `rgba(150,140,230,.28)` (Kanten) · `--on-void` `#E7E5F2` (Text auf dunkel)

**Kategorie-Farben (Graph-Knoten)**
- Allgemeine Psychologie → `#8B7DF0` · Hypnosystemik → `#E8A24A` · Mythos & Psyche → `#6FD3C7`

**Typografie**
- Serif (Fließtext + Überschriften): **Spectral** (Georgia als Fallback)
- Mono/Grotesk (Labels, Navigation, Daten, Graph-UI): **Space Grotesk**
- Eyebrows/Labels: Space Grotesk, GROSSBUCHSTABEN, weit gesperrt (`letter-spacing ~0.16em`)
- Skala (Basis 18px): 15 / 18 / 21 / 27 / 38 / 54 / 76 px

**Raster & Form**
- 4px-Raster: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 px
- Radius: 6 / 12 / 20 px · Pill `999px`
- Schatten: `0 1px 2px rgba(23,20,31,.06), 0 12px 32px rgba(23,20,31,.08)`
- Lesebreite Text 66ch · Layout max 1180px

**Motion**
- Ruhig (150–450ms, `cubic-bezier(.2,.7,.2,1)`). **`prefers-reduced-motion` respektieren.**

## Was es schon gibt (nicht neu erfinden)

- **Seiten:** Startseite (Hero + Graph-Teaser), `/themen` (Grid mit Filter+Suche),
  `/themen/<slug>` (Detail + „verwandte Kräfte"), `/graph` (volle Graph-View), `/ueber`.
- **Komponenten:** Header (sticky, Marke = kleines Kraftfeld-Icon), Footer, TopicCard
  (Kategoriefarbe als Kraftlinie oben), GraphField (force-directed, Drag/Zoom/Hover).
- **Buttons:** `.btn-primary` (Indigo, Pill), `.btn-ghost` (Rand). Labels in Space Grotesk.

Neue Designs sollen sich hier **einfügen**, nicht dagegen arbeiten.

## Content-Modell

Ein Thema = eine Markdown-Datei = ein Graph-Knoten. Frontmatter:
`title`, `summary`, `category` (eine von: Allgemeine Psychologie | Hypnosystemik |
Mythos & Psyche), `tags[]`, `related[]` (Slugs verwandter Themen), `weight`.
Das Feld `related` speist gleichzeitig Graph-Kanten, „verwandte Themen" und Navigation.

## Technischer Rahmen (damit Designs umsetzbar bleiben)

- Astro, statisch. Interaktivität als einzelne „Islands" (Vanilla JS/d3), kein SPA.
- Barrierefreiheit: sichtbarer Fokus, Tastaturbedienung, Screenreader-Fallbacks.
- Responsiv bis Mobile. Keine externen Abhängigkeiten für simple Effekte.
- Texte auf Deutsch, Ton: klar, ruhig, kein Marketing-Sprech; Sie/Du-neutral, eher „du".

## Hand-off zurück an Claude Code (so übergibst du)

Wenn ein Screen sitzt:
1. **Artifact-Code** (HTML/React) bereitstellen.
2. **Screenshot** beilegen.
3. Kurz-Notiz nach dem Muster von `design/HANDOFF.md`:
   *Was ist das? · Wohin gehört es? · Interaktives Verhalten? · Inhalt (echt/Platzhalter)? ·
   Abweichungen/Hinweise?*

## Aufgabe dieses Chats: Landing Page

Entwirf die **Landing Page** in dieser Sprache. Der Hero ist die These — öffne mit dem
Charakteristischsten (das Kraftfeld/Graph-Gedanke). Nutze echte Inhalte aus den Themen
oben, nicht Lorem Ipsum. Halte alles außer dem Signature-Element ruhig.
