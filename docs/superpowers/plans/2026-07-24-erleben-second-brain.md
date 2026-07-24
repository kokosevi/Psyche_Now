# „Erleben" Second-Brain-Wissensgraph — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Baue die Unterseite `/erleben` als interaktive Second-Brain-Wissenskarte der Hypnosystemik — ein gemeinsames Datenmodell, drei live vergleichbare Graph-Varianten und klickbare Konzept-Unterseiten.

**Architecture:** Eine Astro Content Collection (`themen`) hält alle Konzepte als Markdown mit Frontmatter (Cluster, Position, `related`-Wikilinks). Eine reine Funktion `assembleGraph()` normalisiert die Knoten/Kanten (unit-getestet), `buildGraph()` liest die Collection und ruft sie auf. Drei Astro-Komponenten rendern denselben Graph als Konstellation (statisch), Force-Graph (d3-force-Island) und Hybrid (statisch + Progressive Enhancement). Konzept-Unterseiten liegen unter `/erleben/thema/[slug]`.

**Tech Stack:** Astro 7 (static), TypeScript, Astro Content Collections + Zod, `d3-force` (nur in der Force-Island), `vitest` (Unit-Tests), reines CSS + bestehende Tokens aus `homepage.css`.

## Global Constraints

- Alle Arbeit auf Branch `feature/erleben-second-brain` (bereits ausgecheckt).
- Alle Pfade relativ zu `site/` sofern nicht anders angegeben; Befehle aus `site/` ausführen.
- Node `>= 22.12.0` (siehe `package.json` engines).
- **Keine harten Hexwerte** — nur bestehende CSS Custom Properties aus `src/styles/homepage.css` (`--sun`, `--sun-deep`, `--ink`, `--ink-2`, `--ink-3`, `--marker`, `--paper`, `--paper-2`, `--hairline`).
- **Urheberrecht:** alle Konzepttexte sind eigene deutsche Zusammenfassungen — niemals Slides aus `Bibliothek/` kopieren. `Bibliothek/` bleibt gitignored und wird nicht referenziert.
- Sprache Deutsch, `lang="de"`. Labels/Titel in Amatic SC (`var(--font-hand)`), Fließtext in Mulish (`var(--font-sans)`).
- Barrierefrei: Knoten sind `<a>`, tastaturbedienbar, `:focus-visible`-Ring (bestehende Regel greift). `prefers-reduced-motion` stoppt Bewegung.
- Cluster-Enum & Farben (verbindlich): `grundlagen`→`--ink`, `symptom`→`--marker`, `anwendung`→`--sun-deep`, `prozess`→`--ink-2`, `selbst`→`--sun`.
- Commit-Sprache Deutsch; jede Task endet mit Commit inkl. `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

## Knoten-Daten (Single Source of Truth)

Diese Tabelle ist die verbindliche Quelle für Task 2. `full` = voll ausgeschriebener Text (3 Stück), sonst Stub (Frontmatter + Body „Inhalt folgt."). `related` = Slugs (Kanten). `x/y` = %-Position auf dem 100×100-Canvas.

| slug | title | cluster | x | y | status | related | summary |
|---|---|---|---|---|---|---|---|
| erleben-erzeugen | Wie erzeugen wir unser Erleben? | grundlagen | 50 | 30 | full | netzwerk-modell, hirnforschung, trance-transparenz, probleme-basteln | Erleben ist kein Abbild der Realität, sondern ein aktiver innerer Konstruktionsprozess. |
| netzwerk-modell | Das Netzwerk-Modell | grundlagen | 50 | 45 | full | erleben-erzeugen, grundlagenmodell, hirnforschung, utilisation | Psychisches Erleben entsteht aus dem Zusammenspiel vieler innerer Seiten in einem Netzwerk. |
| hirnforschung | Erkenntnisse der Hirnforschung | grundlagen | 40 | 38 | stub | erleben-erzeugen, netzwerk-modell | Das Gehirn arbeitet zustandsabhängig — welche Netze aktiv sind, bestimmt das Erleben. |
| grundlagenmodell | Elementares Grundlagenmodell | grundlagen | 60 | 38 | stub | netzwerk-modell, hypnosystemischer-ansatz | Ein einfaches Modell, wie Aufmerksamkeit, Fokus und Bedeutung zusammenwirken. |
| hypnosystemischer-ansatz | Hypnosystemischer Ansatz auf den Punkt | grundlagen | 44 | 52 | stub | grundlagenmodell, symptomverstaendnis, neutralitaet | Die Verbindung von Hypnotherapie und systemischem Denken in einem Satz. |
| trance-transparenz | Trance & Transparenz | grundlagen | 58 | 52 | stub | erleben-erzeugen, utilisation | Alltagstrancen prägen unser Erleben — Transparenz macht sie nutzbar. |
| probleme-basteln | Bastelanleitung für Probleme | symptom | 82 | 16 | stub | symptomverstaendnis, erleben-erzeugen | Wie wir unbewusst Probleme „herstellen" — und was das über Lösungen verrät. |
| potenzialhypothese | Potenzialhypothese | symptom | 88 | 28 | stub | symptomverstaendnis, zugang-kompetenzen | Hinter jedem Symptom steckt ein übersehenes Potenzial. |
| ursachen | Bedeutung von Ursachen | symptom | 68 | 34 | stub | symptomverstaendnis, diagnosen | Warum die Ursachenfrage in der Beratung oft weniger hilft als gedacht. |
| symptomverstaendnis | Symptomverständnis | symptom | 72 | 20 | stub | potenzialhypothese, ursachen, hypnosystemischer-ansatz | Ein Symptom als sinnvolle Leistung verstehen statt als Defekt. |
| neutralitaet | Neutralität | symptom | 80 | 38 | stub | abgrenzung, hypnosystemischer-ansatz | Allparteilichkeit gegenüber allen inneren Seiten eines Menschen. |
| abgrenzung | Abgrenzungsfähigkeit | symptom | 90 | 44 | stub | neutralitaet, selbstfuersorge | Nähe und Distanz bewusst regulieren, ohne sich zu verlieren. |
| diagnosen | Diagnosen | symptom | 74 | 44 | stub | ursachen, symptomverstaendnis | Diagnosen als Landkarten mit Nutzen und Nebenwirkung. |
| angst | Praxisbeispiel Angst | anwendung | 70 | 60 | stub | symptomverstaendnis, potenzialhypothese | Angst hypnosystemisch verstanden — am konkreten Beispiel. |
| burnout | Burnout | anwendung | 82 | 62 | stub | selbstfuersorge, abgrenzung | Erschöpfung als Signal eines aus der Balance geratenen Systems. |
| entscheidungen | Entscheidungssituationen | anwendung | 90 | 70 | stub | steuerposition, unterschiede | Innere Ambivalenzen als Beratung statt als Blockade nutzen. |
| restriktionen | Umgang mit Restriktionen | anwendung | 68 | 74 | stub | neutralitaet, steuerposition | Handlungsspielraum finden, wo äußere Grenzen eng sind. |
| versoehnung | Das Konzept der Versöhnung | anwendung | 80 | 82 | stub | innere-weisheit, neutralitaet | Frieden schließen mit inneren Seiten, die einander bekämpfen. |
| loesung-aller-probleme | Die Lösung aller Probleme | anwendung | 90 | 84 | stub | potenzialhypothese, innere-weisheit | Ein augenzwinkernder Blick auf die Sehnsucht nach der einen Lösung. |
| beratungssystem | Beratungssystem | prozess | 26 | 60 | stub | auftragsklaerung, steuerposition | Beratung als gemeinsames System aus Klient:in und Beratung. |
| auftragsklaerung | Auftragsklärung | prozess | 14 | 64 | stub | beratungssystem, unterschiede | Woran arbeiten wir eigentlich? Der Auftrag als Kompass. |
| unterschiede | Fokus auf Unterschiede | prozess | 30 | 72 | stub | auftragsklaerung, interventionen | Unterschiede sichtbar machen, die einen Unterschied machen. |
| steuerposition | Aufbau einer Steuerposition | prozess | 18 | 78 | stub | beratungssystem, interventionen | Eine innere Position, von der aus man das eigene Erleben steuert. |
| interventionen | Weitere Interventionen | prozess | 32 | 84 | stub | utilisation, unterschiede | Ein Werkzeugkasten hypnosystemischer Interventionen. |
| utilisation | Utilisation | prozess | 12 | 84 | stub | netzwerk-modell, interventionen, eigene-wahrgebung, trance-transparenz | Alles Vorhandene als Ressource nutzen — auch das „Störende". |
| innere-weisheit | Innere Weisheit | selbst | 20 | 18 | full | zugang-kompetenzen, versoehnung, loesung-aller-probleme | Der Zugang zu einem inneren Wissen, das mehr weiß als der Verstand. |
| zugang-kompetenzen | Optimaler Zugang zu Kompetenzen | selbst | 30 | 26 | stub | innere-weisheit, potenzialhypothese, selbsterfahrung | Vorhandene Fähigkeiten willentlich wieder verfügbar machen. |
| selbstfuersorge | Selbstfürsorge | selbst | 12 | 30 | stub | abgrenzung, burnout, eigene-wahrgebung | Gut für sich sorgen als Grundlage für alles Weitere. |
| eigene-wahrgebung | Utilisation der eigenen Wahrgebung | selbst | 26 | 38 | stub | utilisation, selbstfuersorge | Die eigenen inneren Reaktionen als Informationsquelle nutzen. |
| selbsterfahrung | Selbsterfahrung | selbst | 14 | 42 | stub | zugang-kompetenzen, innere-weisheit | Am eigenen Erleben lernen, wie Hypnosystemik wirkt. |

---

## Task 1: Projekt-Setup (Content-Config, Dependencies, Vitest)

**Files:**
- Create: `site/src/content/config.ts`
- Modify: `site/package.json`
- Create: `site/vitest.config.ts`

**Interfaces:**
- Produces: Collection `themen` mit Zod-Schema; npm-Scripts `test`; Dependencies `d3-force`, `@types/d3-force`, `vitest`.

- [ ] **Step 1: d3-force + vitest installieren**

Run (aus `site/`):
```bash
npm install d3-force@^3.0.0
npm install -D @types/d3-force@^3.0.0 vitest@^2.0.0
```
Expected: `package.json` listet `d3-force` unter dependencies, `@types/d3-force` und `vitest` unter devDependencies.

- [ ] **Step 2: Test-Script in package.json ergänzen**

In `site/package.json` das `scripts`-Objekt um `"test": "vitest run"` und `"test:watch": "vitest"` erweitern (bestehende Scripts behalten).

- [ ] **Step 3: Vitest-Config anlegen**

Create `site/vitest.config.ts`:
```ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['src/**/*.test.ts'],
    environment: 'node',
  },
});
```

- [ ] **Step 4: Content-Collection-Schema anlegen**

Create `site/src/content/config.ts`:
```ts
import { defineCollection, z } from 'astro:content';

export const CLUSTERS = ['grundlagen', 'symptom', 'anwendung', 'prozess', 'selbst'] as const;

const themen = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    cluster: z.enum(CLUSTERS),
    summary: z.string(),
    related: z.array(z.string()).default([]),
    x: z.number().min(0).max(100),
    y: z.number().min(0).max(100),
    status: z.enum(['full', 'stub']).default('stub'),
    lektion: z.number().optional(),
  }),
});

export const collections = { themen };
```

- [ ] **Step 5: Commit**

```bash
cd site && git add package.json package-lock.json vitest.config.ts src/content/config.ts
git commit -m "$(printf 'Erleben: Content-Collection + Test-Setup\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 2: Alle Konzept-Dateien (Daten + 3 Volltexte)

**Files:**
- Create: `site/src/content/themen/<slug>.md` (30 Dateien, ein Slug pro Zeile der Knoten-Tabelle)

**Interfaces:**
- Produces: 30 Collection-Einträge; Slug = Dateiname ohne `.md`.

- [ ] **Step 1: Alle 30 Stub-/Daten-Dateien aus der Knoten-Tabelle erzeugen**

Für **jede** Zeile der Knoten-Tabelle eine Datei `site/src/content/themen/<slug>.md` anlegen. Frontmatter exakt aus der Tabelle (title, cluster, summary, related als YAML-Liste, x, y, status). Für `status: stub` ist der Body genau:
```
Inhalt folgt.
```
Beispiel `site/src/content/themen/hirnforschung.md`:
```markdown
---
title: "Erkenntnisse der Hirnforschung"
cluster: grundlagen
summary: "Das Gehirn arbeitet zustandsabhängig — welche Netze aktiv sind, bestimmt das Erleben."
related: [erleben-erzeugen, netzwerk-modell]
x: 40
y: 38
status: stub
---

Inhalt folgt.
```

- [ ] **Step 2: Volltext „Wie erzeugen wir unser Erleben?"**

Create/overwrite `site/src/content/themen/erleben-erzeugen.md` mit Frontmatter aus der Tabelle (status: full) und diesem Body (eigene Zusammenfassung, keine Zitate):
```markdown
Wir erleben die Welt nicht so, wie sie „an sich" ist. Zwischen dem, was
geschieht, und dem, was wir fühlen, liegt ein aktiver innerer Prozess: Aus
Wahrnehmungen, Erinnerungen, Körperempfindungen und Bewertungen bastelt das
Nervensystem in jedem Moment ein Erleben zusammen. Dasselbe Ereignis kann so für
zwei Menschen — oder für dieselbe Person an zwei Tagen — völlig verschieden
ausfallen.

Für die hypnosystemische Arbeit ist das eine gute Nachricht: Wenn Erleben
gemacht wird, dann lässt es sich auch anders machen. Nicht durch Wegdrücken des
Unangenehmen, sondern indem wir lernen, welche inneren Prozesse gerade welches
Erleben erzeugen — und wie sich Aufmerksamkeit, Fokus und Bedeutung bewusst
verschieben lassen.

Dieses Verständnis ist der Ausgangspunkt der ganzen Karte: Von hier führen die
Fäden zum [Netzwerk-Modell](/erleben/thema/netzwerk-modell), zu den
neurobiologischen Grundlagen und zur Frage, wie Alltagstrancen unser Erleben
prägen.
```

- [ ] **Step 3: Volltext „Das Netzwerk-Modell"**

Create/overwrite `site/src/content/themen/netzwerk-modell.md` (status: full) mit Body:
```markdown
Im hypnosystemischen Denken besteht ein Mensch nicht aus einem einzigen,
einheitlichen „Ich", sondern aus vielen inneren Seiten: Anteilen mit
unterschiedlichen Bedürfnissen, Stimmen, Mustern und Kompetenzen. Erleben
entsteht daraus, welche dieser Seiten in einem Moment aktiviert sind und wie sie
zusammenwirken — wie in einem Netzwerk, in dem mal die einen, mal die anderen
Knoten leuchten.

Ein Symptom ist in diesem Bild selten „die ganze Person", sondern die laute
Meldung einer einzelnen Seite. Andere, ruhigere Seiten tragen oft genau die
Ressourcen, die gerade fehlen. Beratung heißt dann: das Netzwerk sichtbar
machen, überhörte Seiten einladen und die Verbindungen so verändern, dass ein
stimmigeres Erleben möglich wird.

Das Modell ist zugleich das Vorbild dieser Seite: Die Konzepte der Hypnosystemik
selbst bilden ein Netz aus verbundenen Knoten — deshalb kannst du sie hier als
Karte erkunden statt als lineare Liste.
```

- [ ] **Step 4: Volltext „Innere Weisheit"**

Create/overwrite `site/src/content/themen/innere-weisheit.md` (status: full) mit Body:
```markdown
Mit „innerer Weisheit" ist ein Zugang zu einem Wissen gemeint, das tiefer reicht
als das bewusste Nachdenken. Der Körper, die Intuition, das Bauchgefühl — sie
verarbeiten weit mehr Information, als der Verstand in Worte fassen kann. In
Momenten der Ruhe oder der wohlwollenden Selbstzuwendung wird dieses Wissen
zugänglich und kann Orientierung geben, wo das Grübeln im Kreis läuft.

Hypnosystemisch wird innere Weisheit nicht als Esoterik verstanden, sondern als
nutzbare Kompetenz: als eine innere Instanz, die man ansprechen, um Rat fragen
und in Entscheidungen einbeziehen kann. Oft trägt gerade sie die Versöhnung
zwischen widerstreitenden Seiten in sich.

Von hier führen Fäden zum optimalen
[Zugang zu Kompetenzen](/erleben/thema/zugang-kompetenzen) und zum
[Konzept der Versöhnung](/erleben/thema/versoehnung).
```

- [ ] **Step 5: Build prüft das Schema**

Run (aus `site/`): `npm run build`
Expected: Build erfolgreich; keine Zod-Validierungsfehler. (Fehler hier bedeuten Frontmatter-Tippfehler.)

- [ ] **Step 6: Commit**

```bash
cd site && git add src/content/themen
git commit -m "$(printf 'Erleben: 30 Konzept-Knoten (3 voll, Rest Stub)\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 3: Graph-Helper `assembleGraph` + `buildGraph` (TDD)

**Files:**
- Create: `site/src/lib/graph.ts`
- Test: `site/src/lib/graph.test.ts`

**Interfaces:**
- Consumes: Cluster-Namen aus `src/content/config.ts` (Konzept-Ebene) — hier als eigener Typ dupliziert, um Test-Isolation von `astro:content` zu wahren.
- Produces:
  - `type Cluster = 'grundlagen'|'symptom'|'anwendung'|'prozess'|'selbst'`
  - `interface RawNode { slug: string; title: string; cluster: Cluster; summary: string; x: number; y: number; status: 'full'|'stub'; related: string[] }`
  - `interface GraphNode extends RawNode {}`
  - `interface GraphEdge { a: string; b: string }` (a < b lexikografisch)
  - `interface ClusterMeta { id: Cluster; label: string; colorVar: string }`
  - `interface Graph { nodes: GraphNode[]; edges: GraphEdge[]; clusters: ClusterMeta[] }`
  - `function assembleGraph(nodes: RawNode[]): Graph` (rein, wirft bei baumelnden `related`-Slugs)
  - `async function buildGraph(): Promise<Graph>` (liest Collection, ruft `assembleGraph`)

- [ ] **Step 1: Failing test schreiben**

Create `site/src/lib/graph.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { assembleGraph, type RawNode } from './graph';

const n = (slug: string, related: string[] = []): RawNode => ({
  slug, title: slug, cluster: 'grundlagen', summary: 's',
  x: 10, y: 20, status: 'stub', related,
});

describe('assembleGraph', () => {
  it('erzeugt ungerichtete, deduplizierte Kanten (a < b)', () => {
    const g = assembleGraph([n('a', ['b']), n('b', ['a']), n('c')]);
    expect(g.edges).toEqual([{ a: 'a', b: 'b' }]);
  });

  it('wirft bei baumelndem related-Slug', () => {
    expect(() => assembleGraph([n('a', ['ghost'])])).toThrow(/ghost/);
  });

  it('liefert alle fünf Cluster-Metadaten', () => {
    const g = assembleGraph([n('a')]);
    expect(g.clusters.map((c) => c.id)).toEqual(
      ['grundlagen', 'symptom', 'anwendung', 'prozess', 'selbst'],
    );
    expect(g.clusters[1]).toMatchObject({ id: 'symptom', colorVar: '--marker' });
  });

  it('behält alle Knoten', () => {
    const g = assembleGraph([n('a'), n('b')]);
    expect(g.nodes.map((x) => x.slug)).toEqual(['a', 'b']);
  });
});
```

- [ ] **Step 2: Test failen lassen**

Run (aus `site/`): `npm test`
Expected: FAIL — `assembleGraph` bzw. `./graph` nicht gefunden.

- [ ] **Step 3: `graph.ts` implementieren**

Create `site/src/lib/graph.ts`:
```ts
import { getCollection } from 'astro:content';

export type Cluster = 'grundlagen' | 'symptom' | 'anwendung' | 'prozess' | 'selbst';

export interface RawNode {
  slug: string; title: string; cluster: Cluster; summary: string;
  x: number; y: number; status: 'full' | 'stub'; related: string[];
}
export type GraphNode = RawNode;
export interface GraphEdge { a: string; b: string; }
export interface ClusterMeta { id: Cluster; label: string; colorVar: string; }
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[]; clusters: ClusterMeta[]; }

export const CLUSTER_META: ClusterMeta[] = [
  { id: 'grundlagen', label: 'Grundlagen des Erlebens', colorVar: '--ink' },
  { id: 'symptom', label: 'Problem & Symptom', colorVar: '--marker' },
  { id: 'anwendung', label: 'Anwendungsfelder', colorVar: '--sun-deep' },
  { id: 'prozess', label: 'Beratungsprozess', colorVar: '--ink-2' },
  { id: 'selbst', label: 'Selbst & Ressourcen', colorVar: '--sun' },
];

export function assembleGraph(nodes: RawNode[]): Graph {
  const slugs = new Set(nodes.map((x) => x.slug));
  const seen = new Set<string>();
  const edges: GraphEdge[] = [];
  for (const node of nodes) {
    for (const target of node.related) {
      if (!slugs.has(target)) {
        throw new Error(`Baumelnder related-Slug "${target}" in Knoten "${node.slug}"`);
      }
      const [a, b] = [node.slug, target].sort();
      if (a === b) continue;
      const key = `${a}|${b}`;
      if (seen.has(key)) continue;
      seen.add(key);
      edges.push({ a, b });
    }
  }
  return { nodes, edges, clusters: CLUSTER_META };
}

export async function buildGraph(): Promise<Graph> {
  const entries = await getCollection('themen');
  const nodes: RawNode[] = entries.map((e) => ({
    slug: e.slug,
    title: e.data.title,
    cluster: e.data.cluster,
    summary: e.data.summary,
    x: e.data.x,
    y: e.data.y,
    status: e.data.status,
    related: e.data.related,
  }));
  nodes.sort((p, q) => p.slug.localeCompare(q.slug));
  return assembleGraph(nodes);
}
```

- [ ] **Step 4: Tests bestehen lassen**

Run (aus `site/`): `npm test`
Expected: PASS — 4 Tests grün.

- [ ] **Step 5: Commit**

```bash
cd site && git add src/lib/graph.ts src/lib/graph.test.ts
git commit -m "$(printf 'Erleben: Graph-Helper (assembleGraph/buildGraph) + Tests\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 4: Routing-Chirurgie + `/erleben`-Index + Umschalter

**Files:**
- Modify: `site/src/pages/[teil].astro` (getStaticPaths: `erleben` ausschließen)
- Create: `site/src/components/graph/VariantSwitcher.astro`
- Create: `site/src/pages/erleben/index.astro`

**Interfaces:**
- Consumes: `PARTS` aus `src/site.ts`; `buildGraph` aus `src/lib/graph.ts`.
- Produces: `VariantSwitcher` mit Prop `active: 'index'|'konstellation'|'graph'|'hybrid'`; Route `/erleben`.

- [ ] **Step 1: `[teil].astro` gibt `/erleben` ab**

In `site/src/pages/[teil].astro` die `getStaticPaths`-Funktion ändern zu:
```ts
export function getStaticPaths() {
  return PARTS
    .filter((p) => p.id !== 'erleben')
    .map((p) => ({ params: { teil: p.id }, props: { part: p } }));
}
```
(Rest der Datei unverändert.)

- [ ] **Step 2: Verifizieren, dass `/erleben` jetzt kollisionsfrei ist**

Run (aus `site/`): `npm run build`
Expected: Build erfolgreich; `dist/psyche/` und `dist/herausforderungen/` existieren, `dist/erleben/` (noch) nicht (kommt in Step 4). Keine „duplicate route"-Warnung.

- [ ] **Step 3: Umschalter-Komponente**

Create `site/src/components/graph/VariantSwitcher.astro`:
```astro
---
interface Props { active: 'index' | 'konstellation' | 'graph' | 'hybrid'; }
const { active } = Astro.props;
const items = [
  { key: 'konstellation', href: '/erleben/konstellation', label: 'Konstellation' },
  { key: 'graph', href: '/erleben/graph', label: 'Force-Graph' },
  { key: 'hybrid', href: '/erleben/hybrid', label: 'Hybrid' },
] as const;
---
<nav class="switcher" aria-label="Darstellung wählen">
  {items.map((it) => (
    <a href={it.href} aria-current={active === it.key ? 'page' : undefined}>{it.label}</a>
  ))}
</nav>

<style>
  .switcher { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin: 8px 0 24px; }
  .switcher a {
    text-decoration: none; font-weight: 700; font-size: 14px;
    padding: 8px 16px; border-radius: 999px; border: 1px solid var(--hairline);
    color: var(--ink-2); transition: background .18s var(--ease), color .18s var(--ease);
  }
  .switcher a:hover { background: var(--paper-2); }
  .switcher a[aria-current="page"] { background: var(--sun); color: var(--ink); border-color: var(--sun); }
</style>
```

- [ ] **Step 4: `/erleben`-Index (Intro + Umschalter + Cluster-Legende)**

Create `site/src/pages/erleben/index.astro`:
```astro
---
import Site from '../../layouts/Site.astro';
import VariantSwitcher from '../../components/graph/VariantSwitcher.astro';
import { buildGraph } from '../../lib/graph';

const graph = await buildGraph();
---
<Site title="Erleben: Wie Glück gestalten" current="erleben">
  <section class="pagehead wrap">
    <p class="overline">Teil 3</p>
    <h1>Erleben: Wie Glück gestalten</h1>
  </section>
  <section class="wrap erleben-intro">
    <p>
      Die Hypnosystemik versteht Erleben als Netzwerk aus verbundenen inneren
      Seiten. Genau so kannst du sie hier erkunden: als Karte aus Konzepten, die
      miteinander verbunden sind. Wähle eine Darstellung und klicke einen Knoten an.
    </p>
    <VariantSwitcher active="index" />
    <p class="hint">
      Drei Darstellungen zum Vergleich —
      <a href="/erleben/konstellation">Konstellation</a>,
      <a href="/erleben/graph">Force-Graph</a> oder
      <a href="/erleben/hybrid">Hybrid</a>.
    </p>
    <ul class="legende" aria-label="Themenfelder">
      {graph.clusters.map((c) => (
        <li><span class="dot" style={`background: var(${c.colorVar})`}></span>{c.label}</li>
      ))}
    </ul>
  </section>
</Site>

<style>
  .erleben-intro { text-align: center; max-width: 640px; }
  .erleben-intro p { color: var(--ink-2); }
  .erleben-intro .hint { font-size: 14px; color: var(--ink-3); }
  .legende { list-style: none; padding: 0; display: flex; gap: 18px; flex-wrap: wrap; justify-content: center; font-size: 14px; color: var(--ink-2); }
  .legende li { display: flex; align-items: center; gap: 7px; }
  .legende .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
</style>
```

- [ ] **Step 5: Build + Sichtprüfung**

Run (aus `site/`): `npm run build`
Expected: `dist/erleben/index.html` existiert; enthält die Umschalter-Links und die 5 Cluster-Labels.

- [ ] **Step 6: Commit**

```bash
cd site && git add src/pages/[teil].astro src/components/graph/VariantSwitcher.astro src/pages/erleben/index.astro
git commit -m "$(printf 'Erleben: /erleben-Index + Varianten-Umschalter, [teil] gibt erleben ab\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 5: Konzept-Unterseite `/erleben/thema/[slug]`

**Files:**
- Create: `site/src/pages/erleben/thema/[slug].astro`

**Interfaces:**
- Consumes: `getCollection('themen')`, `CLUSTER_META` aus `src/lib/graph.ts`.
- Produces: Route `/erleben/thema/<slug>` je Konzept.

- [ ] **Step 1: Dynamische Seite anlegen**

Create `site/src/pages/erleben/thema/[slug].astro`:
```astro
---
import { getCollection, getEntry } from 'astro:content';
import Site from '../../../layouts/Site.astro';
import { CLUSTER_META } from '../../../lib/graph';

export async function getStaticPaths() {
  const entries = await getCollection('themen');
  return entries.map((e) => ({ params: { slug: e.slug }, props: { entry: e } }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
const cluster = CLUSTER_META.find((c) => c.id === entry.data.cluster)!;

const all = await getCollection('themen');
const related = entry.data.related
  .map((slug) => all.find((e) => e.slug === slug))
  .filter((e): e is NonNullable<typeof e> => Boolean(e));
---
<Site title={entry.data.title} current="erleben">
  <section class="pagehead wrap">
    <p class="overline" style={`color: var(${cluster.colorVar})`}>{cluster.label}</p>
    <h1>{entry.data.title}</h1>
  </section>
  <article class="wrap thema-body">
    <Content />
    {entry.data.status === 'stub' && <p class="stub-hinweis">Dieser Text wird noch ausgeführt.</p>}
  </article>
  {related.length > 0 && (
    <aside class="wrap verwandt" aria-label="Verwandte Konzepte">
      <h2>Verwandte Konzepte</h2>
      <ul>
        {related.map((r) => (
          <li>
            <a href={`/erleben/thema/${r.slug}`}>
              <span class="dot" style={`background: var(${CLUSTER_META.find((c) => c.id === r.data.cluster)!.colorVar})`}></span>
              <strong>{r.data.title}</strong> — {r.data.summary}
            </a>
          </li>
        ))}
      </ul>
    </aside>
  )}
  <p class="wrap zurueck"><a href="/erleben">← Zur Karte</a></p>
</Site>

<style>
  .thema-body { max-width: 640px; }
  .thema-body :global(p) { color: var(--ink-2); }
  .stub-hinweis { color: var(--ink-3); font-style: italic; }
  .verwandt { max-width: 640px; margin-top: 32px; }
  .verwandt h2 { font-family: var(--font-hand); font-size: 30px; }
  .verwandt ul { list-style: none; padding: 0; }
  .verwandt li { border-top: 1px solid var(--hairline); }
  .verwandt a { display: block; padding: 12px 0; text-decoration: none; color: var(--ink-2); font-size: 15px; }
  .verwandt a:hover { color: var(--ink); }
  .verwandt .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }
  .zurueck { max-width: 640px; margin-top: 40px; }
  .zurueck a { font-weight: 700; text-decoration: none; }
</style>
```

- [ ] **Step 2: Build + Prüfung**

Run (aus `site/`): `npm run build`
Expected: `dist/erleben/thema/erleben-erzeugen/index.html` und 29 weitere existieren; die Volltext-Seite enthält den Fließtext, eine Stub-Seite enthält „Inhalt folgt." + „Dieser Text wird noch ausgeführt."

- [ ] **Step 3: Commit**

```bash
cd site && git add src/pages/erleben/thema/[slug].astro
git commit -m "$(printf 'Erleben: Konzept-Unterseiten mit verwandten Konzepten\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 6: Variante 1 — Konstellation (statisch)

**Files:**
- Create: `site/src/components/graph/GraphKonstellation.astro`
- Create: `site/src/pages/erleben/konstellation.astro`

**Interfaces:**
- Consumes: `Graph` aus `buildGraph()`; `VariantSwitcher`.
- Produces: Route `/erleben/konstellation`; Komponente mit Prop `graph: Graph`.

- [ ] **Step 1: Konstellations-Komponente**

Create `site/src/components/graph/GraphKonstellation.astro`:
```astro
---
import type { Graph } from '../../lib/graph';
import { CLUSTER_META } from '../../lib/graph';
interface Props { graph: Graph; }
const { graph } = Astro.props;
const pos = new Map(graph.nodes.map((n) => [n.slug, n]));
const colorOf = (slug: string) =>
  CLUSTER_META.find((c) => c.id === pos.get(slug)!.cluster)!.colorVar;
---
<div class="konstellation" role="group" aria-label="Wissenskarte der Hypnosystemik">
  <svg class="edges" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
    {graph.edges.map((e) => {
      const a = pos.get(e.a)!; const b = pos.get(e.b)!;
      return <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} data-a={e.a} data-b={e.b} />;
    })}
  </svg>
  {graph.nodes.map((n) => (
    <a
      class="node"
      href={`/erleben/thema/${n.slug}`}
      data-slug={n.slug}
      style={`left:${n.x}%; top:${n.y}%; --c: var(${colorOf(n.slug)})`}
    >
      <span class="dot"></span>
      <span class="label">{n.title}</span>
    </a>
  ))}
</div>

<style>
  .konstellation {
    position: relative; width: 100%; aspect-ratio: 3 / 2;
    max-width: 1000px; margin: 0 auto; background: var(--paper-2);
    border-radius: 20px; overflow: hidden;
  }
  .edges { position: absolute; inset: 0; width: 100%; height: 100%; }
  .edges line { stroke: var(--hairline); stroke-width: .4; vector-effect: non-scaling-stroke; }
  .node {
    position: absolute; transform: translate(-50%, -50%);
    display: flex; flex-direction: column; align-items: center; gap: 4px;
    text-decoration: none; color: var(--ink); max-width: 120px; text-align: center;
    transition: transform .18s var(--ease);
  }
  .node .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--c); border: 2px solid var(--paper); box-shadow: var(--shadow-md); }
  .node .label { font-family: var(--font-hand); font-weight: 700; font-size: 17px; line-height: 1.05; }
  .node:hover, .node:focus-visible { transform: translate(-50%, -50%) scale(1.12); z-index: 2; }
  @media (max-width: 720px) { .node .label { font-size: 14px; } .node { max-width: 90px; } }
  @media (prefers-reduced-motion: reduce) { .node { transition: none; } }
</style>
```

- [ ] **Step 2: Konstellations-Seite**

Create `site/src/pages/erleben/konstellation.astro`:
```astro
---
import Site from '../../layouts/Site.astro';
import VariantSwitcher from '../../components/graph/VariantSwitcher.astro';
import GraphKonstellation from '../../components/graph/GraphKonstellation.astro';
import { buildGraph } from '../../lib/graph';
const graph = await buildGraph();
---
<Site title="Erleben — Konstellation" current="erleben">
  <section class="wrap" style="padding-top:32px">
    <VariantSwitcher active="konstellation" />
  </section>
  <section class="wrap">
    <GraphKonstellation graph={graph} />
  </section>
</Site>
```

- [ ] **Step 3: Build + Prüfung**

Run (aus `site/`): `npm run build`
Expected: `dist/erleben/konstellation/index.html` existiert; enthält 30 `.node`-Links und `<line>`-Kanten. `astro check` grün.

- [ ] **Step 4: Commit**

```bash
cd site && git add src/components/graph/GraphKonstellation.astro src/pages/erleben/konstellation.astro
git commit -m "$(printf 'Erleben: Variante 1 — statische Konstellation\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 7: Variante 2 — Force-Graph (d3-force-Island + SSR-Fallback)

**Files:**
- Create: `site/src/components/graph/GraphForce.astro`
- Create: `site/src/pages/erleben/graph.astro`

**Interfaces:**
- Consumes: `Graph` aus `buildGraph()`; `d3-force`.
- Produces: Route `/erleben/graph`; SSR-Linklisten-Fallback + Client-Island.

- [ ] **Step 1: Force-Komponente mit SSR-Fallback + Client-Script**

Create `site/src/components/graph/GraphForce.astro`:
```astro
---
import type { Graph } from '../../lib/graph';
import { CLUSTER_META } from '../../lib/graph';
interface Props { graph: Graph; }
const { graph } = Astro.props;
const colorHexVarName = (cluster: string) => CLUSTER_META.find((c) => c.id === cluster)!.colorVar;
// Serialisierter Graph für die Client-Island (inkl. Cluster-CSS-Var-Name).
const payload = JSON.stringify({
  nodes: graph.nodes.map((n) => ({ slug: n.slug, title: n.title, colorVar: colorHexVarName(n.cluster) })),
  edges: graph.edges,
});
const grouped = CLUSTER_META.map((c) => ({
  meta: c, nodes: graph.nodes.filter((n) => n.cluster === c.id),
}));
---
<div class="force" data-graph={payload}>
  <svg class="force-canvas" aria-hidden="true"></svg>
  <ul class="force-fallback" aria-label="Konzepte nach Themenfeld">
    {grouped.map((g) => (
      <li>
        <span class="grp" style={`color: var(${g.meta.colorVar})`}>{g.meta.label}</span>
        <ul>
          {g.nodes.map((n) => <li><a href={`/erleben/thema/${n.slug}`}>{n.title}</a></li>)}
        </ul>
      </li>
    ))}
  </ul>
</div>

<style>
  .force { width: 100%; max-width: 1000px; margin: 0 auto; }
  .force-canvas { display: none; width: 100%; aspect-ratio: 3 / 2; background: var(--paper-2); border-radius: 20px; touch-action: none; }
  .force.enhanced .force-canvas { display: block; }
  .force.enhanced .force-fallback { display: none; }
  .force-fallback { list-style: none; padding: 0; columns: 2; gap: 24px; }
  .force-fallback > li { break-inside: avoid; margin-bottom: 14px; }
  .force-fallback .grp { font-family: var(--font-hand); font-size: 22px; font-weight: 700; }
  .force-fallback ul { list-style: none; padding: 0; }
  .force-fallback a { text-decoration: none; color: var(--ink-2); font-size: 15px; }
  .force-fallback a:hover { color: var(--ink); }
  :global(.force-node) { cursor: grab; }
  :global(.force-label) { font-family: var(--font-hand); font-size: 13px; fill: var(--ink); pointer-events: none; }
  :global(.force-edge) { stroke: var(--hairline); stroke-width: 1; }
</style>

<script>
  import { forceSimulation, forceLink, forceManyBody, forceCenter, forceCollide } from 'd3-force';

  type N = { slug: string; title: string; colorVar: string; x?: number; y?: number; fx?: number | null; fy?: number | null };
  type E = { a: string; b: string };

  const el = document.querySelector<HTMLElement>('.force');
  if (el && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const data = JSON.parse(el.dataset.graph!) as { nodes: N[]; edges: E[] };
    const svg = el.querySelector<SVGSVGElement>('.force-canvas')!;
    const W = 1000, H = 667;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    const NS = 'http://www.w3.org/2000/svg';

    // Deterministische Startpositionen (kein Math.random): Kreis nach Index.
    data.nodes.forEach((n, i) => {
      const t = (i / data.nodes.length) * Math.PI * 2;
      n.x = W / 2 + Math.cos(t) * 220;
      n.y = H / 2 + Math.sin(t) * 160;
    });
    const bySlug = new Map(data.nodes.map((n) => [n.slug, n]));
    const links = data.edges.map((e) => ({ source: bySlug.get(e.a)!, target: bySlug.get(e.b)! }));

    const gEdges = document.createElementNS(NS, 'g');
    const gNodes = document.createElementNS(NS, 'g');
    svg.append(gEdges, gNodes);
    const lineEls = links.map(() => { const l = document.createElementNS(NS, 'line'); l.setAttribute('class', 'force-edge'); gEdges.append(l); return l; });
    const nodeEls = data.nodes.map((n) => {
      const g = document.createElementNS(NS, 'a') as SVGAElement;
      g.setAttribute('href', `/erleben/thema/${n.slug}`);
      g.setAttribute('class', 'force-node');
      const c = document.createElementNS(NS, 'circle');
      c.setAttribute('r', '9'); c.setAttribute('stroke', 'var(--paper)'); c.setAttribute('stroke-width', '2');
      c.setAttribute('fill', `var(${n.colorVar})`);
      const t = document.createElementNS(NS, 'text');
      t.setAttribute('class', 'force-label'); t.setAttribute('text-anchor', 'middle'); t.setAttribute('dy', '-14');
      t.textContent = n.title;
      g.append(c, t); gNodes.append(g); return { g, c, t, n };
    });

    const sim = forceSimulation(data.nodes as any)
      .force('link', forceLink(links as any).distance(90).strength(.4))
      .force('charge', forceManyBody().strength(-260))
      .force('center', forceCenter(W / 2, H / 2))
      .force('collide', forceCollide(28))
      .on('tick', () => {
        links.forEach((lk, i) => { lineEls[i].setAttribute('x1', lk.source.x!.toString()); lineEls[i].setAttribute('y1', lk.source.y!.toString()); lineEls[i].setAttribute('x2', lk.target.x!.toString()); lineEls[i].setAttribute('y2', lk.target.y!.toString()); });
        nodeEls.forEach(({ g, n }) => g.setAttribute('transform', `translate(${n.x},${n.y})`));
      });

    // Ziehen
    let drag: N | null = null;
    const toSvg = (ev: PointerEvent) => { const r = svg.getBoundingClientRect(); return { x: (ev.clientX - r.left) / r.width * W, y: (ev.clientY - r.top) / r.height * H }; };
    nodeEls.forEach(({ g, n }) => {
      g.addEventListener('pointerdown', (ev) => { ev.preventDefault(); drag = n; sim.alphaTarget(.2).restart(); (g as any).setPointerCapture?.(ev.pointerId); });
    });
    svg.addEventListener('pointermove', (ev) => { if (!drag) return; const p = toSvg(ev); drag.fx = p.x; drag.fy = p.y; });
    svg.addEventListener('pointerup', () => { if (!drag) return; drag.fx = null; drag.fy = null; drag = null; sim.alphaTarget(0); });

    el.classList.add('enhanced');
  }
</script>
```

- [ ] **Step 2: Force-Seite**

Create `site/src/pages/erleben/graph.astro`:
```astro
---
import Site from '../../layouts/Site.astro';
import VariantSwitcher from '../../components/graph/VariantSwitcher.astro';
import GraphForce from '../../components/graph/GraphForce.astro';
import { buildGraph } from '../../lib/graph';
const graph = await buildGraph();
---
<Site title="Erleben — Force-Graph" current="erleben">
  <section class="wrap" style="padding-top:32px">
    <VariantSwitcher active="graph" />
  </section>
  <section class="wrap">
    <GraphForce graph={graph} />
  </section>
</Site>
```

- [ ] **Step 3: Build + Prüfung**

Run (aus `site/`): `npm run build`
Expected: `dist/erleben/graph/index.html` existiert und enthält die SSR-Fallback-Liste (30 Links, nach Cluster gruppiert); `d3-force` wird in ein Insel-Bundle gepackt (Build ohne Fehler). `astro check` grün.

- [ ] **Step 4: Commit**

```bash
cd site && git add src/components/graph/GraphForce.astro src/pages/erleben/graph.astro
git commit -m "$(printf 'Erleben: Variante 2 — Force-Graph (d3-force) mit SSR-Fallback\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 8: Variante 3 — Hybrid (Konstellation + Progressive Enhancement)

**Files:**
- Create: `site/src/pages/erleben/hybrid.astro`

**Interfaces:**
- Consumes: `GraphKonstellation` (aus Task 6), `Graph` aus `buildGraph()`.
- Produces: Route `/erleben/hybrid`; Client-Script veredelt die bestehende Konstellation.

- [ ] **Step 1: Hybrid-Seite (wiederverwendete Konstellation + Enhancement-Script)**

Create `site/src/pages/erleben/hybrid.astro`:
```astro
---
import Site from '../../layouts/Site.astro';
import VariantSwitcher from '../../components/graph/VariantSwitcher.astro';
import GraphKonstellation from '../../components/graph/GraphKonstellation.astro';
import { buildGraph } from '../../lib/graph';
const graph = await buildGraph();
---
<Site title="Erleben — Hybrid" current="erleben">
  <section class="wrap" style="padding-top:32px">
    <VariantSwitcher active="hybrid" />
  </section>
  <section class="wrap hybrid-stage">
    <GraphKonstellation graph={graph} />
  </section>
</Site>

<style>
  /* Sanfte Drift nur im Hybrid, nur mit JS aktiviert (Klasse .drift). */
  .hybrid-stage :global(.konstellation.drift .node) { animation: floaty 6s ease-in-out infinite; }
  .hybrid-stage :global(.konstellation.dim .node) { opacity: .25; transition: opacity .2s var(--ease); }
  .hybrid-stage :global(.konstellation.dim .node.hot) { opacity: 1; }
  .hybrid-stage :global(.konstellation.dim line) { stroke: var(--hairline); }
  .hybrid-stage :global(.konstellation.dim line.hot) { stroke: var(--sun-deep); stroke-width: .9; }
  @keyframes floaty { 0%,100% { transform: translate(-50%,-50%); } 50% { transform: translate(-50%,calc(-50% - 5px)); } }
  @media (prefers-reduced-motion: reduce) {
    .hybrid-stage :global(.konstellation.drift .node) { animation: none; }
  }
</style>

<script>
  const wrap = document.querySelector<HTMLElement>('.hybrid-stage .konstellation');
  if (wrap) {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduce) wrap.classList.add('drift');

    const nodes = Array.from(wrap.querySelectorAll<HTMLElement>('.node'));
    const lines = Array.from(wrap.querySelectorAll<SVGLineElement>('line'));
    const neighbors = new Map<string, Set<string>>();
    lines.forEach((l) => {
      const a = l.dataset.a!, b = l.dataset.b!;
      (neighbors.get(a) ?? neighbors.set(a, new Set()).get(a)!).add(b);
      (neighbors.get(b) ?? neighbors.set(b, new Set()).get(b)!).add(a);
    });

    const highlight = (slug: string | null) => {
      wrap.classList.toggle('dim', slug !== null);
      const hot = slug ? new Set([slug, ...(neighbors.get(slug) ?? [])]) : new Set<string>();
      nodes.forEach((n) => n.classList.toggle('hot', hot.has(n.dataset.slug!)));
      lines.forEach((l) => l.classList.toggle('hot', slug !== null && (l.dataset.a === slug || l.dataset.b === slug)));
    };
    nodes.forEach((n) => {
      n.addEventListener('mouseenter', () => highlight(n.dataset.slug!));
      n.addEventListener('focus', () => highlight(n.dataset.slug!));
      n.addEventListener('mouseleave', () => highlight(null));
      n.addEventListener('blur', () => highlight(null));
    });
  }
</script>
```

- [ ] **Step 2: Build + Prüfung**

Run (aus `site/`): `npm run build`
Expected: `dist/erleben/hybrid/index.html` existiert; enthält dieselbe `.konstellation`-Struktur wie Variante 1 plus das Enhancement-Script. `astro check` grün.

- [ ] **Step 3: Commit**

```bash
cd site && git add src/pages/erleben/hybrid.astro
git commit -m "$(printf 'Erleben: Variante 3 — Hybrid (Konstellation + Highlight/Drift)\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')"
```

---

## Task 9: Gesamt-Verifikation (Build, Tests, A11y-Sichtprüfung)

**Files:** keine neuen — nur Verifikation.

- [ ] **Step 1: Unit-Tests grün**

Run (aus `site/`): `npm test`
Expected: alle Tests PASS.

- [ ] **Step 2: Voller Build + Typecheck**

Run (aus `site/`): `npm run build && npm run check`
Expected: Build ohne Fehler; `astro check` meldet 0 Errors. Erwartete Routen in `dist/`:
`erleben/`, `erleben/konstellation/`, `erleben/graph/`, `erleben/hybrid/`, `erleben/thema/<slug>/` (×30), weiterhin `psyche/`, `herausforderungen/`.

- [ ] **Step 3: Lokale Sichtprüfung (Dev-Server)**

Run (aus `site/`): `npm run dev` und im Browser prüfen:
- `/erleben` zeigt Intro, Umschalter, 5 Cluster-Labels.
- Umschalter wechselt zwischen den drei Varianten; aktiver Link gelb.
- Konstellation: 30 Knoten, Kanten sichtbar, Hover hebt Knoten; Klick → richtige Unterseite.
- Force-Graph: Knoten schwimmen ein, ziehbar; mit deaktiviertem JS bleibt die Cluster-Linkliste.
- Hybrid: Hover hebt verbundenen Teilgraph hervor + gold gefärbte Kanten; Drift sanft.
- Konzept-Seite: Volltext bei den 3 vollen, „verwandte Konzepte" verlinken korrekt, „← Zur Karte" führt zurück.
- Tab-Navigation zeigt Fokusring auf Knoten; bei `prefers-reduced-motion` keine Drift/Physik.

- [ ] **Step 4: Abschluss-Commit (falls Fixes nötig waren)**

```bash
cd site && git add -A
git commit -m "$(printf 'Erleben: Verifikation + Feinschliff\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>')" || echo "nichts zu committen"
```

---

## Self-Review-Ergebnis

- **Spec-Abdeckung:** §2 Datenmodell → Task 1/2/3. §2.2 graph.ts → Task 3. §2.3 Cluster-Farben → Task 3 (`CLUSTER_META`). §3 Knoten-Set → Knoten-Tabelle + Task 2. §4 Routen inkl. `[teil]`-Änderung → Task 4. §4.1 Umschalter → Task 4. §5 drei Varianten → Task 6/7/8. §6 Unterseite → Task 5. §7 A11y/Motion → in jeder Komponente + Task 9. §8 Tests → Task 3 (Unit) + Task 9 (Build/manuell).
- **Placeholder-Scan:** keine offenen TODO/TBD; Volltexte ausgeschrieben; Node-Daten vollständig in der Tabelle.
- **Typkonsistenz:** `Graph/GraphNode/GraphEdge/ClusterMeta/RawNode`, `assembleGraph`/`buildGraph`, `CLUSTER_META`, Prop `graph` und `active` durchgängig identisch benannt.
