import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

export const CLUSTERS = ['grundlagen', 'symptom', 'anwendung', 'prozess', 'selbst'] as const;

const themen = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/themen' }),
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
