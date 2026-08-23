# Handoff: Landingpage „Erleben gestalten" (feelright.ch)

## Überblick
Startseite des Drei-Teile-Projekts. Links Titel + Claim, rechts ein Netz aus drei
kreisrunden Themen-Knoten (Psyche / Herausforderungen / Erleben), verbunden durch
Linien. Die Knoten sind die einzige Navigation in die drei Teile (plus Header/Footer).

## Zu den Design-Dateien
`landingpage.html` ist eine **Design-Referenz in HTML** — ein Prototyp, der Look und
Verhalten zeigt, kein Produktionscode. Aufgabe: das Design im bestehenden
**Astro-7-Projekt** (statisch, Netlify) nachbauen — pures CSS mit Custom Properties
(kein Tailwind), Vanilla-JS-Islands. Die Datei ist bewusst framework-frei gehalten und
lässt sich fast 1:1 in eine .astro-Seite übertragen.

## Fidelity
**High-fidelity.** Farben, Typografie, Abstände, SVG-Geometrie und Icon-Pfade sind final
und sollen pixelgenau übernommen werden. Alle Texte sind final (Deutsch, verbatim
übernehmen).

## Screens / Views

### Landingpage (einzige Seite in diesem Handoff)
**Zweck:** Einstieg; Besucher wählt einen der drei Teile.

**Layout**
- Body: `--paper` Hintergrund, Spectral 18px/1.6, Farbe `--ink`.
- Header: 72px min-height, 1px `--hairline` Border unten. Innen `.wrap`
  (max-width 1200px, padding 0 28px): links Wortmarke „Erleben gestalten"
  (Spectral 600, 19px), rechts 3 Textlinks (Space Grotesk 14px, `--ink-2`,
  hover `--ink`, gap 26px).
- Hero `.held`: CSS-Grid `minmax(300px,5fr) 7fr`, gap 40px, `align-items:center`,
  `min-height:calc(100svh - 73px)`, padding-bottom 40px.
  - Linke Spalte: H1 Spectral 500, `clamp(46px,6vw,80px)`, line-height 1.05,
    letter-spacing -0.01em. Das Wort „Erleben" trägt einen Gelb-Marker via
    `background:linear-gradient(transparent 62%, var(--sun) 62%, var(--sun) 96%, transparent 96%)`,
    padding 0 4px. Darunter Lead: Spectral kursiv 21px, `--ink-2`, margin-top 24px,
    max-width 44ch.
  - Rechte Spalte: SVG-Netz, `viewBox="0 0 800 680"`, width 100%.
- Footer: `--paper-2` Hintergrund, 1px `--hairline` oben, © links, 3 Links rechts
  (Space Grotesk 13px, `--ink-3`).

**SVG-Netz (Geometrie exakt übernehmen)**
- 3 Kanten (Stroke `rgba(30,29,29,.22)`, width 1.5) zwischen den Knotenzentren:
  (190,430)–(430,190), (430,190)–(650,450), (190,430)–(650,450).
- Knoten = `<a>` im SVG mit Kreis `.kern`: fill `--sun`, stroke `--ink` 4px,
  hover-fill `--sun-deep` (transition .18s).
  - Psyche: Zentrum (190,430), r=112 — Icon „settings" (Feather), Labels unterhalb.
  - Herausforderungen: Zentrum (430,190), r=120 — Icon „zap" (Feather), Labels OBERHALB.
  - Erleben: Zentrum (650,450), r=116 — Icon „brush" (Lucide), Labels unterhalb.
- Icons: MIT-lizenzierte 24×24-Pfade, inline im SVG (keine Icon-Fonts), zentriert per
  `translate(cx,cy) scale(s) translate(-12,-12)` mit s = 4.7 / 5.5 / 4.9.
  Stroke `--ink`, round caps/joins; stroke-width lokal 0.85 / 0.73 / 0.82
  → effektiv überall ≈4px (= Kreisrand). Pfade in landingpage.html.
- Knoten-Labels: Space Grotesk 500, 28px, letter-spacing .14em, uppercase, `--ink`;
  Sublabel 23px, `--ink-3`, kein uppercase. Positionen siehe HTML.

**Texte (verbatim)**
- H1: „Erleben gestalten" (Marker auf „Erleben")
- Lead: „Änderst du dein Erleben, ändert sich alles!"
- Knoten: „Psyche / Was wir sind", „Herausforderungen / Woran Glück scheitert",
  „Erleben / Wie Glück gestalten"

## Interaktionen & Verhalten
- Knoten + Header-/Footer-Links → psyche.html / herausforderungen.html / erleben.html
  (in Astro: /psyche usw.).
- Hover Knoten: nur Kreisfüllung `--sun` → `--sun-deep`.
- Ambient: Knoten-Gruppen schweben vertikal ±10px, `ease-in-out infinite`;
  Dauer 7s (.schwebt-a: Psyche + Erleben) bzw. 9s reverse (.schwebt-b: Herausforderungen).
- `prefers-reduced-motion: reduce`: Schweben aus, Hover-Transition aus.
- Fokus: `:focus-visible` 3px `--sun-deep` Outline, offset 4px; Skip-Link
  „Zum Inhalt springen" vor dem Header.
- **Optionales Upgrade (im Prototyp nur als Kommentar markiert):** das statische Netz
  als d3-force-Island (d3-force ist im Projekt) — Knoten leicht federnd, Kanten folgen.
  Positionen/Radien oben als Startwerte verwenden. Bei reduced-motion statisch lassen.

## State Management
Keiner — statische Seite, keine Daten, kein Fetch.

## Responsiv
- ≤900px: Hero einspaltig (Text über Netz), `min-height` aufgehoben, padding 48px 0,
  SVG max-width 560px zentriert. SVG skaliert über viewBox; Texte im SVG skalieren mit.
- Kein Text unter 13px; Knoten sind grosse Touch-Ziele.

## Design-Tokens
```css
--sun:#FBD34D; --sun-deep:#F4B81E; --ink:#1E1D1D; --ink-2:#4A4844; --ink-3:#807C74;
--marker:#ED2A1A; /* reserviert, aktuell ungenutzt */
--paper:#FBFAF7; --paper-2:#F4F1EA; --hairline:#EBE6DB;
```
Schriften (bereits eingebunden): Spectral 400/500/600 + kursiv; Space Grotesk 400/500/700.

## Assets
Keine Bilder. Alle Icons inline-SVG (Feather „settings"/„zap", Lucide „brush", MIT);
Pfade stehen in landingpage.html. Favicon/Logo nicht Teil dieses Handoffs.

## Dateien
- `landingpage.html` — kompletter Prototyp (HTML + CSS in einer Datei, kein JS).
- `PROMPT.md` — fertiger Auftrags-Prompt für Claude Code.
- `screenshot-desktop.png` — Zielbild Desktop (~1200px).
- `screenshot-mobile.png` — Zielbild Mobile (390px, einspaltig).
