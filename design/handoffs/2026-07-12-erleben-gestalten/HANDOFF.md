# Hand-off: Homepage „Erleben gestalten" — v1

Design-Referenz für die Umsetzung in **Astro 7** (statisch, Netlify). Dieses Paket ist
die verbindliche Design-Quelle; alle Dateien hier sind lauffähiges HTML/CSS — im
Browser öffnen und 1:1 vergleichen.

## Was gebaut werden soll

Eine Website mit 4 Seiten:

| Datei (Referenz) | Route | Inhalt |
|---|---|---|
| `index.html` | `/` | Landing Page: Nav + klickbares Dreier-Sujet + Footer |
| `psyche.html` | `/psyche` | Teil 1 — leer (Seitenkopf + Grafik + Platzhalter) |
| `herausforderungen.html` | `/herausforderungen` | Teil 2 — leer (dito) |
| `erleben.html` | `/erleben` | Teil 3 — leer (dito) |

Kernidee der Landing Page: drei Figuren im gleichen Zeichenstil
(physisch → böse → geistig), jede verlinkt auf ihre Unterseite:

1. `bilder/1-psyche.svg` → `/psyche` — „Psyche: Was wir sind" (schwarze Kontur, schaut nach rechts)
2. `bilder/2-herausforderung-animiert.svg` → `/herausforderungen` — „Herausforderungen: Woran Glück scheitert" (rotes Grinsen, animiert)
3. `bilder/3-erleben.svg` → `/erleben` — „Erleben: Wie Glück gestalten" (gelbe Silhouette, schaut nach links)

Unter jeder Grafik: handgezeichneter Strich (inline SVG, 3 Varianten im Markup) + Label in Amatic SC.

## Struktur für Astro (Vorschlag)

- **Ein Layout** (`Layout.astro`): `<head>` mit Fonts, Nav (sticky), `<slot/>`, Footer.
  Nav/Footer sind auf allen 4 Seiten identisch — nur `aria-current="page"` wandert.
- **Kein JS nötig.** Keine Islands, keine Interaktivität ausser Links und CSS-Hover.
  Die Animation steckt komplett im SVG (CSS-Keyframes in der Datei).
- `homepage.css` global einbinden — enthält alle Tokens, Nav, Footer, `.teil`, `.pagehead`.

## Design-Entscheidungen (verbindlich, NICHT durch Spectral/Space Grotesk ersetzen)

- **Schriften:** Avenir (400/500/700/900) + Amatic SC (700), selbst gehostet aus `fonts/`
  (`@font-face` in `homepage.css`). Die bereits eingebundenen Google Fonts der Codebasis
  werden hier bewusst NICHT verwendet. ⚠️ Avenir ist eine kommerzielle Schrift —
  Lizenz für Web-Einbettung vor Launch prüfen.
- **Farben (CSS Custom Properties in `homepage.css`):**
  `--sun #FBD34D` · `--sun-deep #F4B81E` · `--ink #1E1D1D` · `--ink-2 #4A4844` ·
  `--ink-3 #807C74` · `--marker #ED2A1A` · `--paper #FBFAF7` · `--paper-2 #F4F1EA` ·
  `--hairline #EBE6DB`. Keine Hexwerte hart codieren.
- **Typo-Rollen:** Labels/Titel = Amatic SC 700; alles andere = Avenir. Wortmarke =
  Avenir 900, letter-spacing .18em, uppercase.
- **Motion:** Easing `cubic-bezier(.22,1,.36,1)`, 180–220 ms, nur Fades/kleine Lifts.
  Hover auf `.teil`: −6 px translateY, Strich färbt sich `--sun-deep`.

## Die SVGs

- Direkt aus `bilder/` übernehmen, nicht neu zeichnen. Einbettung per `<img>` reicht;
  inline einbetten ist ok (Animation läuft in beiden Fällen).
- `2-herausforderung-animiert.svg`: 5-s-Loop, reine CSS-Animation in der Datei,
  respektiert `prefers-reduced-motion` selbst. Statische Variante liegt bei
  (`2-herausforderung.svg`) — wird auf der Unterseite verwendet.
- Alle Elemente in den SVGs haben IDs (`#figur`, `#grinsen`, `#pfeile` …) für spätere
  Scroll-Animationen.
- `bilder/logo.png` ist **Platzhalter** (Feelgood-Logo) — finales Logo folgt.

## Anforderungen (aus TECH-FOR-DESIGN.md, hier bereits umgesetzt)

- Responsiv bis Mobile: Sujet-Grid bricht bei ≤ 860 px auf 1 Spalte; Wortmarke
  verschwindet bei ≤ 720 px (nur Logo).
- Barrierefrei: sichtbarer Fokus (`:focus-visible`, 3 px `--sun-deep`), alles per
  Tastatur erreichbar (nur `<a>`-Elemente), Alt-Texte auf allen Grafiken,
  Strich-SVGs `aria-hidden="true"`.
- `prefers-reduced-motion`: Hover-Lifts und Smooth-Scroll aus; SVG-Animation stoppt selbst.
- Sprache Deutsch, `lang="de"`.

## Abnahme-Checkliste

1. Landing zeigt drei Figuren nebeneinander (Desktop) bzw. untereinander (Mobile).
2. Klick/Enter auf jede Figur führt zur richtigen Unterseite; aktiver Nav-Link gelb.
3. Grinsen animiert im 5-s-Loop; bei `prefers-reduced-motion: reduce` statisch.
4. Hover: Figur hebt sich, Strich wird gold. Fokusring sichtbar bei Tab-Navigation.
5. Pixel-Vergleich gegen `index.html` in diesem Ordner.
