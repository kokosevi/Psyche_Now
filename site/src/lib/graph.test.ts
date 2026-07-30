import { describe, it, expect } from 'vitest';
import { assembleGraph, PSYCHE_CLUSTER_META, type RawNode } from './graph';

const n = (slug: string, related: string[] = []): RawNode => ({
  slug, title: slug, cluster: 'k1', summary: 's',
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

  it('liefert alle vier Kapitel-Cluster-Metadaten', () => {
    const g = assembleGraph([n('a')]);
    expect(g.clusters.map((c) => c.id)).toEqual(['k1', 'k2', 'k3', 'k4']);
    expect(g.clusters[1]).toMatchObject({ id: 'k2', colorVar: '--marker' });
  });

  it('behält alle Knoten', () => {
    const g = assembleGraph([n('a'), n('b')]);
    expect(g.nodes.map((x) => x.slug)).toEqual(['a', 'b']);
  });

  it('liefert die fünf Psyche-Cluster-Metadaten', () => {
    const p = (slug: string): RawNode => ({
      slug, title: slug, cluster: 'p1', summary: 's', x: 10, y: 20, status: 'stub', related: [],
    });
    const g = assembleGraph([p('a')], PSYCHE_CLUSTER_META);
    expect(g.clusters.map((c) => c.id)).toEqual(['p1', 'p2', 'p3', 'p4', 'p5']);
    expect(g.clusters[1]).toMatchObject({ id: 'p2', colorVar: '--marker' });
  });
});
