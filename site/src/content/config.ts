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
