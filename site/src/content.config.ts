import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Ein Thema = eine Markdown-Datei = ein Knoten im Graph.
// Das Feld `related` speist gleichzeitig: Graph-Kanten, "verwandte Themen" und Navigation.
const themen = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/themen' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    // Taxonomie -> Eyebrow-Label + Filter.
    category: z.enum([
      'Allgemeine Psychologie',
      'Hypnosystemik',
      'Mythos & Psyche',
    ]),
    tags: z.array(z.string()).default([]),
    // Slugs verwandter Themen -> Kanten im Graph + "verwandte Themen".
    related: z.array(z.string()).default([]),
    // Reihenfolge/Wichtigkeit (größer = zentraler im Feld).
    weight: z.number().default(1),
    draft: z.boolean().default(false),
  }),
});

export const collections = { themen };
