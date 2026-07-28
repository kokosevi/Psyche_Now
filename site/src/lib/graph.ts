export type Cluster = 'k1' | 'k2' | 'k3' | 'k4';

export interface RawNode {
  slug: string; title: string; cluster: Cluster; summary: string;
  x: number; y: number; status: 'full' | 'stub'; related: string[];
}
export type GraphNode = RawNode;
export interface GraphEdge { a: string; b: string; }
export interface ClusterMeta { id: Cluster; label: string; colorVar: string; }
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[]; clusters: ClusterMeta[]; }

export const CLUSTER_META: ClusterMeta[] = [
  { id: 'k1', label: 'Grundlagen', colorVar: '--ink' },
  { id: 'k2', label: 'Herausforderungen', colorVar: '--marker' },
  { id: 'k3', label: 'Handwerk', colorVar: '--ink-2' },
  { id: 'k4', label: 'Praxisfälle', colorVar: '--sun-deep' },
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
  const { getCollection } = await import('astro:content');
  const entries = await getCollection('themen');
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
  return assembleGraph(nodes);
}
