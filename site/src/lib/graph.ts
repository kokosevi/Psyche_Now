// Cluster-IDs sind je Raum verschieden (Erleben: k1–k4, Herausforderungen: h1–h4),
// daher generisch als string typisiert. Die konkrete Menge steckt in der jeweiligen
// ClusterMeta-Liste.
export type Cluster = string;

export interface RawNode {
  slug: string; title: string; cluster: Cluster; summary: string;
  x: number; y: number; status: 'full' | 'stub'; related: string[];
}
export type GraphNode = RawNode;
export interface GraphEdge { a: string; b: string; }
export interface ClusterMeta { id: Cluster; label: string; colorVar: string; }
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[]; clusters: ClusterMeta[]; }

// Raum „Erleben" (Hypnosystemik-Kurs).
export const CLUSTER_META: ClusterMeta[] = [
  { id: 'k1', label: 'Grundlagen', colorVar: '--leaf' },
  { id: 'k2', label: 'Herausforderungen', colorVar: '--marker' },
  { id: 'k3', label: 'Handwerk', colorVar: '--ink-2' },
  { id: 'k4', label: 'Praxisfälle', colorVar: '--sun-deep' },
];

// Raum „Herausforderungen: Woran Glück scheitert". Labels/Zuordnung sind eine erste
// Fassung und werden bei der Kuratierung finalisiert (Cluster-Zuordnung im
// heraus_manifest der Pipeline).
export const HERAUS_CLUSTER_META: ClusterMeta[] = [
  { id: 'h1', label: 'Innere Fallen', colorVar: '--marker' },
  { id: 'h2', label: 'Beziehung & Vergleich', colorVar: '--sun-deep' },
  { id: 'h3', label: 'Sinn & Werte', colorVar: '--leaf' },
  { id: 'h4', label: 'Reizwelt & Struktur', colorVar: '--ink-2' },
];

export function assembleGraph(nodes: RawNode[], clusters: ClusterMeta[] = CLUSTER_META): Graph {
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
  return { nodes, edges, clusters };
}

export type CollectionName = 'themen' | 'herausforderungen';

export async function buildGraph(
  collection: CollectionName = 'themen',
  clusters: ClusterMeta[] = CLUSTER_META,
): Promise<Graph> {
  const { getCollection } = await import('astro:content');
  const entries = await getCollection(collection);
  const nodes: RawNode[] = entries.map((e) => ({
    slug: e.id,
    title: e.data.title,
    cluster: e.data.cluster,
    summary: e.data.summary,
    x: e.data.x,
    y: e.data.y,
    status: e.data.status,
    related: e.data.related,
  }));
  nodes.sort((p, q) => p.slug.localeCompare(q.slug));
  return assembleGraph(nodes, clusters);
}
