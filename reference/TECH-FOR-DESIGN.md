# Technischer Rahmen für Claude Design

> Kurzes Merkblatt: **womit** die Seite gebaut wird. Damit deine Design-Hand-offs
> direkt umsetzbar sind. (Optik/Design-System steht separat — hier geht es nur um Stack
> und Sprachen.) Ins Claude.ai-Projektwissen legen.

## Stack

- **Astro** (Version 7), **statische** Ausgabe. Kein SPA, kein Server, keine Datenbank.
- Gehostet auf **Netlify**, Statistik über **Umami**.
- **Kein** Login, **keine** Zahlung, **keine** Registrierung.

## Sprachen

- **HTML** + **CSS** (reines CSS mit Custom Properties / Design-Tokens — **kein**
  Tailwind, Bootstrap oder anderes CSS-Framework).
- **Vanilla JavaScript** für Interaktivität, als einzelne Astro-„Islands".
  (Für den Graphen ist `d3-force` bereits im Projekt.)
- Build-Dateien sind TypeScript — für Designs aber nicht nötig.

## Hand-off-Format

- Liefere den Screen als **Artifact**: **HTML/CSS** bevorzugt, **React** ist auch ok.
  Beides wird hier in **Astro + Vanilla JS** übersetzt — baue also nichts, das zwingend
  React-Runtime braucht (kein Redux, keine schweren UI-Kits).
- **Icons:** inline **SVG**, keine Icon-Fonts.
- **Bilder:** als Platzhalter markieren; echte Assets kommen im Code dazu.

## Was die Umsetzung voraussetzt (bitte mitdenken)

- **Responsiv** bis Mobile.
- **Barrierefrei:** sichtbarer Fokus, Tastaturbedienung, sinnvolle Alternativtexte.
- **`prefers-reduced-motion`** respektieren (Animationen abschaltbar).
- **Schriften:** Google Fonts **Spectral** (Serif) + **Space Grotesk** (Labels) — schon eingebunden.
- **Inhaltssprache: Deutsch.**
- Abhängigkeiten sparsam halten — simple Effekte ohne externe Libraries lösen.
