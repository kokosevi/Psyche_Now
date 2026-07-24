import { describe, it, expect } from 'vitest';
import { assembleGraph, type RawNode } from './graph';

const n = (slug: string, related: string[] = []): RawNode => ({
  slug, title: slug, cluster: 'grundlagen', summary: 's',
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

  it('liefert alle fünf Cluster-Metadaten', () => {
    const g = assembleGraph([n('a')]);
    expect(g.clusters.map((c) => c.id)).toEqual(
      ['grundlagen', 'symptom', 'anwendung', 'prozess', 'selbst'],
    );
    expect(g.clusters[1]).toMatchObject({ id: 'symptom', colorVar: '--marker' });
  });

  it('behält alle Knoten', () => {
    const g = assembleGraph([n('a'), n('b')]);
    expect(g.nodes.map((x) => x.slug)).toEqual(['a', 'b']);
  });
});
