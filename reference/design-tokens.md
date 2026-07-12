# Design-Tokens — Richtung «Kraftfeld»

> ⚠️ **Überholt (Stand 2026-07-12).** Das live umgesetzte Design ist inzwischen
> **«Erleben gestalten»** aus dem Claude-Design-Hand-off
> (`design/handoffs/2026-07-12-erleben-gestalten/`). Die verbindlichen Tokens leben jetzt in
> **`site/src/styles/homepage.css`** (Sonnengelb-Palette, Avenir + Amatic SC). Dieses
> «Kraftfeld»-Dokument bleibt nur als frühe Design-Notiz erhalten.

Die **gemeinsame Sprache** von Claude Design und Claude Code. Farben, Schriften und
Abstände sind hier *einmal* definiert. In Claude Design benennst du sie beim Namen
("Hintergrund = `--paper`"), im Code liegen exakt dieselben Werte
(`site/src/styles/tokens.css`) — so sieht das Gebaute aus wie dein Mockup.

## Die Idee dahinter

Psyche als **Feld aus wirkenden Kräften** — hergeleitet aus dem Quellmaterial
(Bischof, *Das Kraftfeld der Mythen*; Hypnosystemik: Ambivalenz, Pole, innere Anteile).
Zwei Pole in Spannung geben die Palette vor: **Indigo** (Tiefe/Unbewusstes) und
**Bernstein** (Energie/Ladung). Der Themen-**Graph** ist das Signature-Element und lebt
auf tiefem Nachtindigo.

> Bewusst **nicht** der übliche „warmes Creme + Terrakotta-Serif"-Look. Verfeinere in
> Claude Design; wenn es sitzt, aktualisieren wir diese Datei.

---

## Farben — Lesemodus (helle Flächen)

| Token         | Wert       | Verwendung                             |
|---------------|------------|----------------------------------------|
| `--paper`     | `#EEECF4`  | Seitenhintergrund (kühles Lila-Grau)   |
| `--surface`   | `#FBFAFE`  | Karten, erhöhte Flächen                |
| `--ink`       | `#17141F`  | Haupttext (fast schwarz, leicht violett)|
| `--muted`     | `#6C6879`  | Sekundärtext, Labels                   |
| `--line`      | `#DCD9E6`  | Trennlinien, Kartenränder              |
| `--indigo`    | `#443A8E`  | Links, Buttons, primärer Akzent (Pol 1)|
| `--indigo-soft`| `#EAE7F6` | zarte Indigo-Fläche (Hover, Chips)     |
| `--amber`     | `#B5621C`  | Hervorhebung, aktiver Zustand (Pol 2)  |

## Farben — Feldmodus (Graph, dunkel)

| Token          | Wert       | Verwendung                         |
|----------------|------------|------------------------------------|
| `--void`       | `#0C0E1A`  | Graph-Hintergrund (Nachtindigo)    |
| `--void-2`     | `#151A33`  | Panels auf dem Feld                |
| `--node`       | `#8B7DF0`  | Knoten (leuchtendes Indigo)        |
| `--node-hot`   | `#E8A24A`  | aktiver/gehighlighteter Knoten     |
| `--edge`       | `rgba(150,140,230,.28)` | Kanten/Kraftlinien    |
| `--on-void`    | `#E7E5F2`  | Text auf dunklem Feld              |

## Schrift

| Token          | Wert                                   | Verwendung                |
|----------------|----------------------------------------|---------------------------|
| `--font-serif` | "Spectral", Georgia, serif             | Fließtext, Überschriften  |
| `--font-mono`  | "Space Grotesk", system-ui, sans-serif | Labels, Nav, Daten, Graph-UI |

Literarische Serif trifft technisch-instrumenthafte Grotesk. Labels/Eyebrows in
`--font-mono`, GROSSBUCHSTABEN, weit gesperrt — kodieren die echte Taxonomie
(z. B. „HYPNOSYSTEMIK").

**Skala** (Basis 18px): `--text-sm` 15px · `--text-base` 18px · `--text-lg` 21px ·
`--text-xl` 27px · `--text-2xl` 38px · `--text-3xl` 54px · `--text-4xl` 76px

## Raster, Radius, Schatten

Abstände (4px-Raster): `--space-1…16` = 4/8/12/16/24/32/48/64px
Radius: `--radius-sm` 6px · `--radius-md` 12px · `--radius-lg` 20px · `--radius-pill` 999px
Schatten: `--shadow-card` = `0 1px 2px rgba(23,20,31,.06), 0 12px 32px rgba(23,20,31,.08)`
Breiten: `--max-prose` 66ch · `--max-page` 1180px

## Motion

Übergänge ruhig (150–450ms, `ease`/`cubic-bezier(.2,.7,.2,1)`). Graph-Physik läuft
kontinuierlich. **`prefers-reduced-motion` wird respektiert** (keine Reveals, Graph
startet statisch positioniert).
