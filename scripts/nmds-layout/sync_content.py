"""Baut den veröffentlichten Content aus den Knotenordnern.

Quelle je Knoten: Bibliothek/Hypnosystemik/<nummer>-<slug>/
  meta.json   -> title, summary, status, (hero, heroAlt)
  text.md     -> Body (Fertigtext); fehlt/leer => Stub "Inhalt folgt."
  *.{jpg,png,…} -> werden in den Content-Ordner kopiert (gehen live)

Berechnet: cluster (manifest), x/y (out/layout.json), related (out/edges.curated.json).
Ausgabe: site/src/content/themen/<slug>/index.md (generierter Output — nicht von
Hand editieren; hier wird alles überschrieben).

Ersetzt das frühere write_frontmatter.py (Body kam dort aus dem Content selbst).
"""
import os, re, json, glob, shutil
from manifest import NODES
from extract_corpus import folder_name

HERE = os.path.dirname(__file__)
BIB = os.path.normpath(os.path.join(HERE, "..", "..", "Bibliothek", "Hypnosystemik"))
THEMEN = os.path.normpath(os.path.join(HERE, "..", "..", "site", "src", "content", "themen"))

layout = json.load(open(os.path.join(HERE, "out", "layout.json")))
curated = json.load(open(os.path.join(HERE, "out", "edges.curated.json")))

rel = {}
for a, b in curated:
    rel.setdefault(a, set()).add(b)
    rel.setdefault(b, set()).add(a)

MEDIA = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg", ".mp4", ".webm"}


def render(meta, cluster, x, y, related, body, hero, hero_alt):
    rel_s = "[" + ", ".join(sorted(set(related))) + "]"
    lines = ["---",
             f'title: "{meta["title"]}"',
             f"cluster: {cluster}",
             f'summary: "{meta["summary"]}"',
             f"related: {rel_s}",
             f"x: {x}",
             f"y: {y}",
             f"status: {meta['status']}"]
    if hero:
        lines.append(f"hero: ./{hero}")
    if hero_alt:
        lines.append(f'heroAlt: "{hero_alt}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def main():
    written = 0
    copied = 0
    for nd in NODES:
        slug = nd["slug"]
        src = os.path.join(BIB, folder_name(nd))
        outdir = os.path.join(THEMEN, slug)
        os.makedirs(outdir, exist_ok=True)

        meta = json.load(open(os.path.join(src, "meta.json"), encoding="utf-8"))

        tp = os.path.join(src, "text.md")
        body = ""
        if os.path.exists(tp):
            body = open(tp, encoding="utf-8").read().strip()
        if not body:
            body = "Inhalt folgt."

        # Medien in den Content-Ordner kopieren (nur so gehen sie über GitHub live)
        for path in sorted(glob.glob(os.path.join(src, "*"))):
            if os.path.splitext(path)[1].lower() in MEDIA:
                shutil.copy2(path, os.path.join(outdir, os.path.basename(path)))
                copied += 1

        x = layout[slug]["x"]
        y = layout[slug]["y"]
        related = sorted(rel.get(slug, set()))
        out = render(meta, nd["cluster"], x, y, related, body,
                     meta.get("hero"), meta.get("heroAlt"))
        open(os.path.join(outdir, "index.md"), "w", encoding="utf-8").write(out)
        written += 1
    print(f"Content generiert: {written} Seiten, {copied} Mediendateien kopiert")


if __name__ == "__main__":
    main()
