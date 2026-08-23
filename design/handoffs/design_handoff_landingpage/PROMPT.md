# Prompt für Claude Code

Setze die Landingpage von feelright.ch („Erleben gestalten") nach der beiliegenden
Design-Referenz um.

## Auftrag
Baue die Startseite als Astro-7-Seite (statische Ausgabe) in diesem Projekt nach.
Vorlage: `landingpage.html` in diesem Ordner — eine High-Fidelity-Design-Referenz
(HTML + CSS in einer Datei, kein JS). Übernimm Layout, Farben, Typografie, Texte und
die komplette SVG-Geometrie pixelgenau; `README.md` dokumentiert alle Details,
`screenshot-desktop.png` / `screenshot-mobile.png` zeigen das Zielbild.

## Regeln
- Astro 7, statisch. Pures CSS mit den Custom Properties aus dem README als
  Design-Tokens (kein Tailwind, kein CSS-Framework, keine neuen Abhängigkeiten).
- Schriften Spectral + Space Grotesk sind im Projekt schon eingebunden — nutze die
  bestehende Einbindung, keine zweite.
- Icons bleiben inline-SVG (Pfade aus der Vorlage übernehmen), keine Icon-Fonts.
- Inhaltssprache Deutsch; alle Texte verbatim aus der Vorlage.
- Links der drei Knoten sowie Header/Footer zeigen auf die bestehenden Routen
  /psyche, /herausforderungen, /erleben (Routen-Namen ggf. an das Projekt anpassen).
- Barrierefrei: Skip-Link, :focus-visible-Ring, aria-labels der Knoten,
  Tastatur-Navigation durch die drei SVG-Links.
- prefers-reduced-motion: Schweb-Animation und Hover-Transition deaktivieren
  (steht so in der Vorlage).
- Responsiv wie in der Vorlage: unter 900px einspaltig, Netz max. 560px zentriert.

## Optional (nur wenn ohne Mehraufwand sauber machbar)
Das statische Netz-SVG als kleines Vanilla-JS-Island mit d3-force (ist im Projekt):
die drei Knoten leicht federnd, Kanten folgen den Positionen. Startpositionen und
Radien aus der Vorlage; bei prefers-reduced-motion statisch bleiben. Wenn das den
Rahmen sprengt: statisches SVG mit der CSS-Schweb-Animation aus der Vorlage.

## Abnahme-Checkliste
- [ ] Desktop ≥1200px: Hero füllt Viewport-Höhe, Text links, Netz rechts.
- [ ] „Erleben" trägt den gelben Marker-Hintergrund.
- [ ] Hover Knoten: Füllung #FBD34D → #F4B81E, sonst nichts.
- [ ] Labels: Herausforderungen oberhalb, Psyche/Erleben unterhalb des Kreises.
- [ ] Mobile 390px: einspaltig, kein horizontales Scrollen.
- [ ] Lighthouse: keine Kontrast- oder Fokus-Beanstandungen.
