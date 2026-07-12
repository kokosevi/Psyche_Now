# Design-Tokens

Die **gemeinsame Sprache** von Claude Design und Claude Code. Hier sind Farben,
Schriften und Abstände *einmal* definiert. In Claude Design benennst du sie
("Hintergrund = `--color-bg`"), im Code sind exakt dieselben Werte hinterlegt —
so sieht das gebaute Ergebnis aus wie dein Mockup.

> Dies ist ein **Startpunkt**. Verfeinere Palette und Schriften in Claude Design;
> wenn sie sitzen, aktualisieren wir diese Datei — sie bleibt die Quelle der Wahrheit.

---

## Farben

Ruhige, nachdenkliche Palette — warme Neutraltöne, tiefe „Tinte", ein Akzent.

| Token             | Wert       | Verwendung                          |
|-------------------|------------|-------------------------------------|
| `--color-bg`      | `#F7F4EF`  | Seitenhintergrund (warmes Papier)   |
| `--color-surface` | `#FFFFFF`  | Karten, erhöhte Flächen             |
| `--color-ink`     | `#1F1B16`  | Haupttext (fast schwarz, warm)      |
| `--color-muted`   | `#6B6459`  | Sekundärtext, Beschriftungen        |
| `--color-accent`  | `#3A5A66`  | Links, Buttons, Graph-Kanten (Petrol)|
| `--color-accent-2`| `#B5643C`  | Hervorhebung, aktive Knoten (Terrakotta)|
| `--color-border`  | `#E3DDD3`  | Trennlinien, Kartenränder           |

**Dark Mode** (optional, später):
| `--color-bg` `#17140F` · `--color-surface` `#211D17` · `--color-ink` `#EDE7DC` · `--color-accent` `#7FA8B4` |

## Schrift

| Token           | Wert                                   | Verwendung          |
|-----------------|----------------------------------------|---------------------|
| `--font-serif`  | z. B. "Fraunces", Georgia, serif       | Überschriften, Zitate |
| `--font-sans`   | z. B. "Inter", system-ui, sans-serif   | Fließtext, UI       |

**Skala** (Fließtext 18px als Basis):
`--text-sm` 15px · `--text-base` 18px · `--text-lg` 22px · `--text-xl` 28px · `--text-2xl` 40px · `--text-3xl` 56px

## Abstände

4px-Raster: `--space-1` 4px · `--space-2` 8px · `--space-3` 12px · `--space-4` 16px ·
`--space-6` 24px · `--space-8` 32px · `--space-12` 48px · `--space-16` 64px

## Radius & Schatten

`--radius-sm` 6px · `--radius-md` 12px · `--radius-lg` 20px
`--shadow-card` `0 1px 3px rgba(31,27,22,.08), 0 8px 24px rgba(31,27,22,.06)`

## Maximale Breiten

`--max-prose` 68ch (Lesetext) · `--max-page` 1200px (Layout)

---

## Als CSS (kommt beim Scaffold in `site/src/styles/tokens.css`)

```css
:root {
  --color-bg: #F7F4EF;
  --color-surface: #FFFFFF;
  --color-ink: #1F1B16;
  --color-muted: #6B6459;
  --color-accent: #3A5A66;
  --color-accent-2: #B5643C;
  --color-border: #E3DDD3;

  --font-serif: "Fraunces", Georgia, serif;
  --font-sans: "Inter", system-ui, -apple-system, sans-serif;

  --text-sm: .9375rem; --text-base: 1.125rem; --text-lg: 1.375rem;
  --text-xl: 1.75rem; --text-2xl: 2.5rem; --text-3xl: 3.5rem;

  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;

  --radius-sm: 6px; --radius-md: 12px; --radius-lg: 20px;
  --shadow-card: 0 1px 3px rgba(31,27,22,.08), 0 8px 24px rgba(31,27,22,.06);

  --max-prose: 68ch; --max-page: 1200px;
}
```
