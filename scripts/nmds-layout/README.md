# Erleben-Karte & Content-Pipeline

Jede Subpage ist ein **Knotenordner** unter `Bibliothek/Hypnosystemik/<nummer>-<slug>/`
(lokal, gitignored — teils urheberrechtlich geschütztes Quellmaterial). Aus diesen
Ordnern werden **beide** Dinge erzeugt: die Distanzen/Kanten der Erleben-Karte und
der veröffentlichte Content.

## Ordnerkonvention

```
Bibliothek/Hypnosystemik/4.2.4-depression/
  quelle.md    Roh-Transkript o. Notizen. Fließt in die Karte, geht NIE live.
  text.md      Fertiger, eigenständiger Seitentext (Body). Fehlt/leer => Stub.
  meta.json    { "title", "summary", "status": "full"|"stub", "hero"?, "heroAlt"? }
  hero.jpg …   Bilder/Animationen. Werden in den Content kopiert und gehen live.
```

- **Nummer** = TOC-Nummer aus `manifest.py` (heading-key, Buchstaben-Suffix entfernt).
- **Karte** rechnet aus ALLEN `*.md` im Ordner (quelle + text), mit relativer
  Häufigkeit (Längen-Normalisierung) — `tfidf.py`.
- **Urheberrecht:** `quelle.md` (Transkript) bleibt lokal. Der veröffentlichte
  `text.md` muss ein eigenständiger Text sein, kein Verbatim-Transkript.

## Rebuild (nach jeder Ordner-Änderung)

```
scripts/nmds-layout/rebuild.sh      # build_layout → curate_edges → sync_content
cd site && npm run build            # Seite bauen/prüfen
```

Determiniert (NMDS seed=42) und idempotent: gleiche Ordner → gleiche Karte/Content.

## Skripte

| Skript | Aufgabe |
|--------|---------|
| `build_layout.py`  | NMDS-Positionen + Kantenvorschläge aus den Ordnern → `out/layout.json`, `out/edges.suggested.json` |
| `curate_edges.py`  | Kanten kuratieren (Grad-Deckel, jeder Knoten ≥1 Kante) → `out/edges.curated.json` |
| `sync_content.py`  | `site/src/content/themen/<slug>/index.md` + Medien erzeugen |
| `extract_corpus.py`| Corpus je Knoten (alle `*.md` im Ordner) |
| `tfidf.py`         | TF-IDF mit relativer Häufigkeit + Cosinus |
| `manifest.py`      | Feste Taxonomie: slug → cluster, TOC-Nummer, Titel |

`site/src/content/themen/` ist **generierter Output** — nicht von Hand editieren;
Änderungen gehören in die Bibliothek-Ordner.
