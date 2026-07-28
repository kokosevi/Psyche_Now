# Ordner-pro-Subpage für Themen-Content

**Datum:** 2026-07-28
**Ziel:** Jede Subpage (Themen-Knoten) wird ein eigener Ordner, damit finale,
live sichtbare Assets (Bilder, später Animationen) ko-lokalisiert neben dem Text
liegen und mitgebaut/optimiert werden.

## Struktur (alle 50 Knoten)

```
site/src/content/themen/<slug>/
  index.md      ← bisheriger <slug>.md-Inhalt, unverändert
  (künftig: hero.jpg, grafik-1.png, intro.mp4 …)
```

## Änderungen

1. **Migration:** `git mv site/src/content/themen/<slug>.md
   site/src/content/themen/<slug>/index.md` für alle 50 (History bleibt).

2. **`site/src/content.config.ts`:**
   - Glob-Loader bekommt `generateId`, sodass der **Ordnername der Slug** ist
     (`depression/index.md → id "depression"`). Kritisch: `e.id` ist überall der
     Slug (`graph.ts:43`, `thema/[slug].astro`, `related`-Links).
   - Schema auf Funktionsform (`({ image }) => z.object({…})`) umstellen und
     optionale, ko-lokalisierte Medienfelder ergänzen:
     `hero: image().optional()`, `heroAlt: z.string().optional()`.
   - Fließtext-Bilder (`![](./bild.png)`) werden von Astro automatisch optimiert.

3. **`scripts/nmds-layout/write_frontmatter.py`:** Zielpfad → `<slug>/index.md`
   (Verzeichnis anlegen). Hält die NMDS-Kartenpipeline funktionsfähig.

4. **`scripts/nmds-layout/set_summaries.py`:** Zielpfad → `<slug>/index.md`.

## Bewusst NICHT jetzt (YAGNI)

- Keine format-spezifische Animations-Einbindung (Video/GIF/Lottie) — es gibt
  noch keine Animation. Konvention (Datei in den Subpage-Ordner) wird nur
  dokumentiert; die Verdrahtung folgt, sobald die erste Animation existiert.

## Verifikation

- `npm run build`: **identische 54 Routen**, insbesondere alle
  `/erleben/thema/<slug>` unverändert (Slug-Erhaltung bewiesen).
- `npx vitest run` grün.
- Stichprobe: eine Fall-Subpage lädt korrekt; `git log --follow` zeigt History
  über den Move hinweg.
