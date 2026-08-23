// Abnahme-Tests für die Landingpage (design/handoffs/design_handoff_landingpage).
// Rendert die echte Seite über Astros Container-API und prüft alle Punkte der
// Checkliste, die sich im HTML verifizieren lassen.
// Baut die Site (astro build) und liest dist/index.html — testet damit exakt das,
// was Netlify ausliefert. (Astros Container-API scheitert an Vitest-2/Vite-Konflikt.)
import { describe, it, expect, beforeAll } from 'vitest';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
let html = '';

beforeAll(() => {
  execSync('npx astro build', { cwd: root, stdio: 'pipe' });
  html = readFileSync(join(root, 'dist', 'index.html'), 'utf8');
});

describe('Landingpage — Hero', () => {
  it('H1 mit Marker-<em> auf «Erleben»', () => {
    expect(html).toMatch(/<h1[^>]*><em[^>]*>Erleben<\/em> gestalten<\/h1>/);
  });

  it('Lead verbatim', () => {
    expect(html).toContain('Änderst du dein Erleben, ändert sich alles!');
  });
});

describe('Landingpage — SVG-Netz', () => {
  it('drei Kanten mit exakter Geometrie', () => {
    expect(html).toMatch(/x1="190"[^>]*y1="430"[^>]*x2="430"[^>]*y2="190"/);
    expect(html).toMatch(/x1="430"[^>]*y1="190"[^>]*x2="650"[^>]*y2="450"/);
    expect(html).toMatch(/x1="190"[^>]*y1="430"[^>]*x2="650"[^>]*y2="450"/);
  });

  it('drei Knoten-Links auf die Projekt-Routen mit aria-labels', () => {
    expect(html).toMatch(/href="\/psyche"[^>]*aria-label="Teil 1 – Psyche: Was wir sind"|aria-label="Teil 1 – Psyche: Was wir sind"[^>]*href="\/psyche"/);
    expect(html).toMatch(/href="\/herausforderungen"[^>]*aria-label="Teil 2 – Herausforderungen: Woran Glück scheitert"|aria-label="Teil 2 – Herausforderungen: Woran Glück scheitert"[^>]*href="\/herausforderungen"/);
    expect(html).toMatch(/href="\/erleben"[^>]*aria-label="Teil 3 – Erleben: Wie Glück gestalten"|aria-label="Teil 3 – Erleben: Wie Glück gestalten"[^>]*href="\/erleben"/);
  });

  it('Kreise: Zentren und Radien exakt aus der Vorlage', () => {
    expect(html).toMatch(/cx="190"[^>]*cy="430"[^>]*r="112"/);
    expect(html).toMatch(/cx="430"[^>]*cy="190"[^>]*r="120"/);
    expect(html).toMatch(/cx="650"[^>]*cy="450"[^>]*r="116"/);
  });

  it('Labels: Herausforderungen oberhalb (y<190), Psyche/Erleben unterhalb', () => {
    expect(html).toMatch(/y="28"[^>]*>Herausforderungen</);
    expect(html).toMatch(/y="578"[^>]*>Psyche</);
    expect(html).toMatch(/y="600"[^>]*>Erleben</);
    // Sublabels verbatim
    expect(html).toContain('Was wir sind');
    expect(html).toContain('Woran Glück scheitert');
    expect(html).toContain('Wie Glück gestalten');
  });

  it('Icons inline mit exakter Zentrierung (translate/scale) und Feather-zap-Polygon', () => {
    expect(html).toContain('translate(190,430) scale(4.7) translate(-12,-12)');
    expect(html).toContain('translate(430,190) scale(5.5) translate(-12,-12)');
    expect(html).toContain('translate(650,450) scale(4.9) translate(-12,-12)');
    expect(html).toContain('13 2 3 14 12 14 11 22 21 10 12 10 13 2'); // zap
  });
});

describe('Header & Footer (sitewide neu)', () => {
  it('Wortmarke ohne Logo-Bild, Nav-Links auf die drei Teile', () => {
    expect(html).toMatch(/<a class="marke[^"]*" href="\/">Erleben gestalten<\/a>/);
    expect(html).not.toMatch(/<header[^>]*>[\s\S]*?<img[\s\S]*?<\/header>/); // kein Logo im Header
  });

  it('Skip-Link vorhanden', () => {
    expect(html).toContain('Zum Inhalt springen');
  });

  it('Footer mit © und den drei Teil-Links', () => {
    expect(html).toContain('© 2026 Erleben gestalten');
    expect(html).toMatch(/<footer[\s\S]*href="\/psyche"[\s\S]*href="\/herausforderungen"[\s\S]*href="\/erleben"[\s\S]*<\/footer>/);
  });
});
