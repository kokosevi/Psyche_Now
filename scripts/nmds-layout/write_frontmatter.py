import json, os, re
from manifest import NODES

HERE = os.path.dirname(__file__)
THEMEN = os.path.normpath(os.path.join(HERE, "..", "..", "site", "src", "content", "themen"))
layout = json.load(open(os.path.join(HERE, "out", "layout.json")))
curated = json.load(open(os.path.join(HERE, "out", "edges.curated.json")))

rel_from_edges = {}
for a, b in curated:
    rel_from_edges.setdefault(a, set()).add(b)
    rel_from_edges.setdefault(b, set()).add(a)

FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def parse_related(fm_text):
    m = re.search(r"^related:\s*\[(.*?)\]\s*$", fm_text, re.M)
    if not m or not m.group(1).strip():
        return []
    return [x.strip().strip('"').strip("'") for x in m.group(1).split(",") if x.strip()]


def parse_field(fm_text, key, default=""):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm_text, re.M)
    return m.group(1) if m else default


def render(title, cluster, x, y, summary, related, status, body):
    rel = "[" + ", ".join(sorted(set(related))) + "]"
    fm = (f'---\ntitle: "{title}"\ncluster: {cluster}\n'
          f'summary: "{summary}"\nrelated: {rel}\n'
          f'x: {x}\ny: {y}\nstatus: {status}\n---\n')
    return fm + body


def main():
    created, updated = 0, 0
    for nd in NODES:
        slug = nd["slug"]
        pos = layout[slug]
        path = os.path.join(THEMEN, slug + ".md")
        edge_rel = rel_from_edges.get(slug, set())
        if os.path.exists(path):
            raw = open(path, encoding="utf-8").read()
            m = FM.match(raw)
            fm_text, body = m.group(1), m.group(2)
            title = parse_field(fm_text, "title", nd["title"])
            summary = parse_field(fm_text, "summary", "")
            status = parse_field(fm_text, "status", "stub")
            # related wird ERSETZT = nur die (neu berechneten) cluster-übergreifenden
            # Kanten; alte/Intra-Cluster-Kanten fallen weg (Nähe steckt in x/y).
            related = sorted(edge_rel)
            updated += 1
        else:
            title = nd["title"]
            summary = f"{title} — Zusammenfassung folgt."
            status = "stub"
            body = "\nInhalt folgt.\n"
            related = sorted(edge_rel)
            created += 1
        out = render(title, pos["cluster"], pos["x"], pos["y"],
                     summary, related, status, body)
        open(path, "w", encoding="utf-8").write(out)
    print(f"Frontmatter geschrieben: {len(NODES)} Dateien ({updated} aktualisiert, {created} neu)")


if __name__ == "__main__":
    main()
