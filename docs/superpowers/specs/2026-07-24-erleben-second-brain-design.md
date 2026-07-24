# Design: „Erleben" als Second-Brain-Wissensgraph

**Datum:** 2026-07-24
**Seite:** `/erleben` (Teil 3 — „Erleben: Wie Glück gestalten")
**Referenz-Idee:** Second Brain / Obsidian-Graph (Karpathy, via mattpaige68.substack.com) —
Wissen als Netz aus verlinkten Konzept-Knoten.
**Quelle des Inhalts:** `Bibliothek/Hypnosystemik/` (Gunther Schmidt, „Hypnosystemische
Therapie & Beratung", lifelessons.de). ⚠️ Urheberrechtlich geschützt — **nur eigene
Zusammenfassungen** veröffentlichen, nie Slides kopieren. `Bibliothek/` bleibt gitignored.

## 1. Ziel & Umfang

Die Unterseite `/erleben` wird zu einer **interaktiven Wissenskarte** der Hypnosystemik:
Konzepte als Knoten, Beziehungen als Kanten. Klick auf einen Knoten → eigene
Konzept-Unterseite. Passend zur Sache: Schmidts Modell ist selbst ein **„Netzwerk-Modell"**
des Erlebens — die Graph-Darstellung spiegelt die Theorie.

**Dieser Bau liefert ein Walking Skeleton:**
- **Drei live vergleichbare Graph-Varianten** (kuratierte Konstellation, Force-Graph, Hybrid),
  damit der Nutzer die beste Darstellung im Browser auswählen kann.
- **Alle ~30 Konzepte** als Knoten (aus den Lektionen der Slides).
- **3 voll ausgeschriebene** Konzept-Unterseiten als Vorlage:
  „Wie erzeugen wir unser Erleben?", „Netzwerk-Modell", „Innere Weisheit".
- **Rest als Stubs** (Titel + Summary + „Inhalt folgt"), voll navigierbar.

**Nicht in diesem Bau:** finale Auswahl einer Variante (kommt nach Vergleich); Volltexte aller
Konzepte; Fonts/Animation der Startseite (bleiben wie live: Mulish + MP4).

## 2. Gemeinsames Fundament — ein Datenmodell, drei Ansichten

### 2.1 Content Collection

Neues Verzeichnis `site/src/content/themen/` mit einer Markdown-Datei je Konzept.
`site/src/content/config.ts` definiert die Collection `themen` mit Zod-Schema:

```ts
// site/src/content/config.ts
import { defineCollection, z } from 'astro:content';

const CLUSTERS = ['grundlagen', 'symptom', 'anwendung', 'prozess', 'selbst'] as const;

const themen = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    cluster: z.enum(CLUSTERS),
    summary: z.string(),                 // 1 Satz, für Hover/Stub/related-Liste
    related: z.array(z.string()).default([]),  // slugs anderer Konzepte = Kanten
    x: z.number().min(0).max(100),       // %-Position (kuratierte Konstellation)
    y: z.number().min(0).max(100),
    status: z.enum(['full', 'stub']).default('stub'),
    lektion: z.number().optional(),      // Herkunft (Slide-Lektion), nur Referenz
  }),
});

export const collection = { themen };
```

Der **Slug** ergibt sich aus dem Dateinamen (`erleben-erzeugen.md` → `erleben-erzeugen`).
`related` enthält Slugs — diese sind die Wikilinks/Kanten.

### 2.2 Graph-Helper

`site/src/lib/graph.ts` liest die Collection und liefert ein normalisiertes Graph-Objekt,
das **alle drei Varianten und die Konzept-Unterseiten** konsumieren:

```ts
export interface GraphNode {
  slug: string; title: string; cluster: Cluster; summary: string;
  x: number; y: number; status: 'full' | 'stub'; related: string[];
}
export interface GraphEdge { a: string; b: string; }  // ungerichtet, a<b, dedupliziert
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[]; clusters: ClusterMeta[]; }

export async function buildGraph(): Promise<Graph>;
```

Regeln:
- Kanten aus `related`, **beidseitig** normalisiert (A→B und B→A ergeben eine Kante),
  Duplikate entfernt, Reihenfolge (a,b) alphabetisch stabil.
- **Integritätsregel:** jeder `related`-Slug muss auf einen existierenden Knoten zeigen —
  sonst Build-Fehler (siehe Tests). Keine baumelnden Wikilinks.
- `ClusterMeta` hält Label + Token-Farbe je Cluster.

### 2.3 Cluster & Farben (bestehende Tokens)

| Cluster       | Label (Amatic)              | Farbe (Token) |
|---------------|-----------------------------|---------------|
| `grundlagen`  | Grundlagen des Erlebens     | `--ink`       |
| `symptom`     | Problem & Symptom           | `--marker`    |
| `anwendung`   | Anwendungsfelder            | `--sun-deep`  |
| `prozess`     | Beratungsprozess            | `--ink-2`     |
| `selbst`      | Selbst & Ressourcen         | `--sun`       |

Keine neuen Hexwerte — nur bestehende Custom Properties aus `homepage.css`.

## 3. Knoten-Set (alle Lektionen)

Aus den Lektions-Titeln der Slides abgeleitet (Lektion 1 „Kursüberblick" = Meta, wird als
Intro genutzt, nicht als Knoten). ~30 Konzepte in 5 Clustern:

**grundlagen:** Hypnosystemischer Ansatz auf den Punkt (L7) · Wie erzeugen wir unser Erleben? (L9,**full**) ·
Erkenntnisse der Hirnforschung (L10) · Elementares Grundlagenmodell (L11) ·
Netzwerk-Modell (L12/13,**full**) · Trance & Transparenz (L14)

**symptom:** Bastelanleitung für Probleme (L16) · Potenzialhypothese (L17) ·
Bedeutung von Ursachen (L18) · Symptomverständnis (L19) · Neutralität (L20) ·
Abgrenzungsfähigkeit (L21) · Diagnosen (L22)

**anwendung:** Praxisbeispiel Angst (L8) · Burnout (L23) · Entscheidungssituationen (L24) ·
Umgang mit Restriktionen (L25) · Das Konzept der Versöhnung (L26) · Die Lösung aller Probleme (L27)

**prozess:** Beratungssystem (L29) · Auftragsklärung (L31) · Fokus auf Unterschiede (L32) ·
Aufbau einer Steuerposition (L34) · Weitere Interventionen (L35) · Utilisation (L36)

**selbst:** Selbsterfahrung (L15) · Selbstfürsorge (L41) · Utilisation der eigenen „Wahrgebung" (L42) ·
Optimaler Zugang zu Kompetenzen (L43) · Innere Weisheit (L46,**full**)

Kanten werden pro Datei in `related` von Hand gesetzt (fachlich sinnvolle Nähe, cluster-intern
und clusterübergreifend). `x/y`-Positionen so gewählt, dass Cluster als „Sternbilder"
räumlich zusammenliegen.

## 4. Routen & Seiten

| Route | Datei | Inhalt |
|---|---|---|
| `/erleben` | `pages/erleben/index.astro` | Intro + Umschalter, zeigt Standard-Variante (Konstellation) |
| `/erleben/konstellation` | `pages/erleben/konstellation.astro` | Variante 1 |
| `/erleben/graph` | `pages/erleben/graph.astro` | Variante 2 |
| `/erleben/hybrid` | `pages/erleben/hybrid.astro` | Variante 3 |
| `/erleben/thema/[slug]` | `pages/erleben/thema/[slug].astro` | Konzept-Unterseite |

**Wichtige bestehende Änderung:** `pages/[teil].astro` erzeugt aktuell auch `/erleben`.
`getStaticPaths` dort muss `erleben` **ausschließen** (nur `psyche`, `herausforderungen`
bleiben), damit `pages/erleben/index.astro` die Route `/erleben` übernimmt. Nav/Footer
verlinken weiter auf `/erleben` — unverändert.

Konzept-Seiten liegen unter `/erleben/thema/…` (nicht `/erleben/[slug]`), um Kollisionen mit
den reservierten Varianten-Routen `konstellation`/`graph`/`hybrid` sicher auszuschließen.

### 4.1 Umschalter (Vergleichs-UX)

Kleine, wiederverwendbare `VariantSwitcher.astro`-Komponente (Segmented Control, 3 Links).
Auf jeder Varianten-Seite oben eingebunden; markiert die aktive Variante
(`aria-current="page"`). Reiner Link-Umschalter, kein JS.

## 5. Die drei Graph-Varianten

Alle rendern serverseitig aus `buildGraph()`. Gemeinsame Sub-Komponenten:
`GraphNode.astro` (Knoten-Link) und die Kanten-Pfade.

**Variante 1 — Konstellation (`GraphKonstellation.astro`):**
- Ein `<svg viewBox="0 0 100 100" preserveAspectRatio>`-Canvas (responsiv, `width:100%`).
- Kanten = `<path>`/`<line>` zwischen `x/y`-Punkten, Marker-Stil (leicht handgezeichnet,
  `--hairline`/`--ink-3`).
- Knoten = HTML-Overlay aus `<a>`-Elementen (absolut positioniert per `%`), Label in Amatic SC,
  Cluster-Farbpunkt. Klick → `/erleben/thema/<slug>`.
- Nur CSS-Interaktion: Hover/Focus → Knoten hebt sich (−4px), zugehörige Kanten werden gold
  (`--sun-deep`). Kein JS.

**Variante 2 — Force-Graph (`GraphForce.astro` + Insel `force-graph.ts`):**
- Astro-Insel (`client:load`), `d3-force` (neue Dependency, isoliert in dieser Insel).
- SVG, Kräfte-Simulation, Knoten ziehbar, Pan/Zoom, Hover hebt Nachbarn hervor.
- **Barrierefreier Fallback:** dieselben Knoten werden serverseitig als
  gruppierte `<ul>`-Linkliste gerendert; die Insel ersetzt sie erst nach dem Mount.
  Ohne JS bleibt die Liste bestehen.
- Deterministischer Seed für die Startanordnung (kein `Math.random` beim Build).

**Variante 3 — Hybrid (`GraphHybrid.astro` + Insel `hybrid-enhance.ts`):**
- Basis = exakt Variante-1-Markup (SSR, ohne JS voll funktionsfähig).
- Progressive Enhancement (`client:idle`, Vanilla-JS): Hover/Focus hebt den **verbundenen
  Teilgraph** hervor; sanfte Drift-Animation der Knoten; optional leichtes Ziehen mit
  Rückfederung.
- `prefers-reduced-motion` schaltet Drift/Animation ab; ohne JS = Variante 1.

## 6. Konzept-Unterseite (`/erleben/thema/[slug]`)

- `getStaticPaths` aus der `themen`-Collection.
- Nutzt bestehende `.pagehead`-Styles: Cluster-Label als Overline, Titel in Amatic SC,
  darunter der gerenderte Markdown-Body (`<Content />`).
- **„Verwandte Konzepte":** Liste der `related`-Knoten (Titel + Summary) als Links — die
  Wikilink-Navigation. Zusätzlich „← Zur Karte" (zurück zu `/erleben`).
- Stub-Seiten: Overline + Titel + Summary + Hinweis „Inhalt folgt" + verwandte Konzepte.
- Voll-Seiten (3): eigener, in Severins Stimme geschriebener Fließtext (Zusammenfassung, keine
  Slide-Zitate).

## 7. Barrierefreiheit & Motion

- Alle Knoten sind `<a>` — tastaturbedienbar, `:focus-visible`-Ring (bestehende Regel).
- Force-Graph hat SSR-Linklisten-Fallback; Hybrid degradiert auf statisch.
- `prefers-reduced-motion`: Drift/Physik/Lifts aus (bestehende Media-Query erweitern).
- Cluster-Farbe nie alleiniger Bedeutungsträger — immer mit Text-Label gepaart.
- `lang="de"`, sinnvolle `aria-label` an den Graph-Regionen.

## 8. Tests / Verifikation

- **Unit (vitest) für `buildGraph()`:** (a) Kanten sind ungerichtet & dedupliziert;
  (b) jeder `related`-Slug existiert als Knoten (kein baumelnder Link) — sonst Fehler;
  (c) jeder Knoten hat `x/y` in [0,100]; (d) Cluster-Enum eingehalten.
- **Content-Schema:** Zod validiert beim Build (`astro build` schlägt bei Verstoß fehl).
- **Build-Smoke:** `npm run build` erzeugt `/erleben`, die drei Varianten und je eine
  `thema`-Seite pro Konzept ohne Fehler; `astro check` grün.
- **Manuell:** Umschalter wechselt Varianten; Klick auf Knoten führt zur richtigen Unterseite;
  Force-Graph zeigt ohne JS die Linkliste; reduced-motion stoppt Bewegung.

## 9. Dateien (neu/geändert)

**Neu:** `content/config.ts` · `content/themen/*.md` (~30) · `lib/graph.ts` ·
`components/graph/VariantSwitcher.astro` · `GraphKonstellation.astro` · `GraphForce.astro` ·
`GraphHybrid.astro` · `GraphNode.astro` · Inseln `force-graph.ts`, `hybrid-enhance.ts` ·
`pages/erleben/index.astro` · `konstellation.astro` · `graph.astro` · `hybrid.astro` ·
`pages/erleben/thema/[slug].astro` · Graph-CSS (in `homepage.css` oder eigenes Modul) ·
`lib/graph.test.ts`.
**Geändert:** `pages/[teil].astro` (erleben ausschließen) · `package.json` (`d3-force`,
Dev: `vitest`).

## 10. Offene Punkte für später

- Auswahl der finalen Variante nach dem Vergleich → dann werden die anderen zwei Routen
  entfernt und die Gewinner-Ansicht wird `/erleben`.
- Restliche ~27 Konzepttexte ausschreiben (Severins Stimme).
- Feinschliff `x/y`-Positionen / Kanten-Kuratierung.
