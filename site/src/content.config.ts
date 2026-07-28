import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

export const CLUSTERS = ['k1', 'k2', 'k3', 'k4'] as const;

const themen = defineCollection({
  // Jede Subpage ist ein Ordner: themen/<slug>/index.md (+ ko-lokalisierte Assets).
  // generateId hält den Slug = Ordnername, damit id stabil bleibt (e.id wird überall
  // als Slug genutzt: related-Links, Kartenkanten/-positionen, /erleben/thema/<slug>).
  loader: glob({
    pattern: '**/index.md',
    base: './src/content/themen',
    generateId: ({ entry }) => entry.replace(/\/index\.md$/, ''),
  }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      cluster: z.enum(CLUSTERS),
      summary: z.string(),
      related: z.array(z.string()).default([]),
      x: z.number().min(0).max(100),
      y: z.number().min(0).max(100),
      status: z.enum(['full', 'stub']).default('stub'),
      lektion: z.number().optional(),
      // Optionale, neben index.md liegende Medien (werden von Astro optimiert).
      hero: image().optional(),
      heroAlt: z.string().optional(),
    }),
});

export const collections = { themen };
