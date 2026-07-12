import type { CollectionEntry } from 'astro:content';

export type Category =
  | 'Allgemeine Psychologie'
  | 'Hypnosystemik'
  | 'Mythos & Psyche';

export interface GraphNode {
  id: string;
  title: string;
  category: Category;
  weight: number;
  url: string;
}

export interface GraphLink {
  source: string;
  target: string;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

/** Farbe pro Kategorie — passt zu den Design-Tokens (Feldmodus). */
export const categoryColor: Record<Category, string> = {
  'Allgemeine Psychologie': '#8B7DF0', // --node (Indigo)
  Hypnosystemik: '#E8A24A',            // --node-hot (Bernstein)
  'Mythos & Psyche': '#6FD3C7',        // ergänzender Pol (Teal)
};

/**
 * Baut aus den Themen-Einträgen einen ungerichteten Graphen.
 * Kanten kommen aus `related`; doppelte (A→B und B→A) werden zusammengefasst.
 */
export function buildGraph(entries: CollectionEntry<'themen'>[]): GraphData {
  const known = new Set(entries.map((e) => e.id));

  const nodes: GraphNode[] = entries.map((e) => ({
    id: e.id,
    title: e.data.title,
    category: e.data.category,
    weight: e.data.weight,
    url: `/themen/${e.id}`,
  }));

  const seen = new Set<string>();
  const links: GraphLink[] = [];
  for (const e of entries) {
    for (const target of e.data.related) {
      if (!known.has(target)) continue; // verwaiste Referenz überspringen
      const key = [e.id, target].sort().join('::');
      if (seen.has(key)) continue;
      seen.add(key);
      links.push({ source: e.id, target });
    }
  }

  return { nodes, links };
}
