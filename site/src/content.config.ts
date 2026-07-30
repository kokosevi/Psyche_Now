import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

export const CLUSTERS = ['k1', 'k2', 'k3', 'k4'] as const;
export const HERAUS_CLUSTERS = ['h1', 'h2', 'h3', 'h4'] as const;
export const PSYCHE_CLUSTERS = ['p1', 'p2', 'p3', 'p4', 'p5'] as const;

// Gemeinsames Schema für beide Karten-Räume; nur der Cluster-Enum unterscheidet sich.
// `image` ist der von Astro im schema-Callback gereichte Image-Helfer.
const themaSchema = (clusters: readonly [string, ...string[]], image: any) =>
  z.object({
    title: z.string(),
    cluster: z.enum(clusters),
    summary: z.string(),
    related: z.array(z.string()).default([]),
    x: z.number().min(0).max(100),
    y: z.number().min(0).max(100),
    status: z.enum(['full', 'stub']).default('stub'),
    lektion: z.number().optional(),
    // Optionale, neben index.md liegende Medien (werden von Astro optimiert).
    hero: image().optional(),
    heroAlt: z.string().optional(),
  });

// Jede Subpage ist ein Ordner: <collection>/<slug>/index.md (+ ko-lokalisierte Assets).
// generateId hält den Slug = Ordnername, damit id stabil bleibt (e.id wird überall als
// Slug genutzt: related-Links, Kartenkanten/-positionen, .../thema/<slug>).
const slugFromIndex = ({ entry }: { entry: string }) => entry.replace(/\/index\.md$/, '');

const themen = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './src/content/themen', generateId: slugFromIndex }),
  schema: ({ image }) => themaSchema(CLUSTERS, image),
});

const herausforderungen = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './src/content/herausforderungen', generateId: slugFromIndex }),
  schema: ({ image }) => themaSchema(HERAUS_CLUSTERS, image),
});

const psyche = defineCollection({
  loader: glob({ pattern: '**/index.md', base: './src/content/psyche', generateId: slugFromIndex }),
  schema: ({ image }) => themaSchema(PSYCHE_CLUSTERS, image),
});

export const collections = { themen, herausforderungen, psyche };
