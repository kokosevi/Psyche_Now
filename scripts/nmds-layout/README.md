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

## Zwei Räume

Es gibt zwei unabhängige Karten (konfiguriert in `spaces.py`, gewählt per Env-Var
`SPACE`, Default `erleben`):

| Raum | Quelle | Content-Collection | Cluster |
|------|--------|--------------------|---------|
| `erleben` | `Bibliothek/Hypnosystemik/` | `site/src/content/themen/` | k1–k4 |
| `herausforderungen` | `Bibliothek/Herausforderungen/` | `site/src/content/herausforderungen/` | h1–h4 |

Knotenliste + Titel je Raum: `manifest.py` (Erleben) bzw. `heraus_manifest.py`
(Herausforderungen). Cluster-Labels/-Farben der Site: `site/src/lib/graph.ts`.

## Rebuild (nach jeder Ordner-Änderung)

```
scripts/nmds-layout/rebuild.sh [raum]   # raum = erleben (Default) | herausforderungen
cd site && npm run build                # Seite bauen/prüfen
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
