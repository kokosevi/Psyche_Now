// Zentrale Definition der drei Teile — Nav, Footer und Landing-Sujet lesen von hier.
export type PartId = 'psyche' | 'herausforderungen' | 'erleben';

export interface Part {
  id: PartId;
  href: string;
  nav: string; // kurzer Nav-Titel
  label: string; // langer Titel (Sujet-Label / Seitenkopf)
  overline: string; // "Teil 1" …
  image: string; // statische Grafik
  imageAnim: string; // animierte Grafik (nur Landing)
  alt: string;
  strich: string; // handgezeichneter Strich-Pfad (SVG path d)
  intro: string; // Platzhaltertext auf der Unterseite
}

export const PARTS: Part[] = [
  {
    id: 'psyche',
    href: '/psyche',
    nav: 'Psyche',
    label: 'Psyche: Was wir sind',
    overline: 'Teil 1',
    image: '/bilder/1-psyche.svg',
    imageAnim: '/bilder/1-psyche.svg',
    alt: 'Sitzende Figur als schwarze Kontur – das Grundgerüst der Psyche',
    strich: 'M 5 9 C 40 3 78 12 118 7 C 152 3 190 8 215 7',
    intro: 'Hier entsteht das allgemeinpsychologische Grundmodell (nach Norbert Bischof). Inhalt folgt.',
  },
  {
    id: 'herausforderungen',
    href: '/herausforderungen',
    nav: 'Herausforderungen',
    label: 'Herausforderungen: Woran Glück scheitert',
    overline: 'Teil 2',
    image: '/bilder/2-herausforderung.svg',
    imageAnim: '/bilder/2-herausforderung-animiert.svg',
    alt: 'Rotes, böses Grinsen zwischen gegenläufigen Pfeilen',
    strich: 'M 5 7 C 44 11 80 4 120 8 C 156 11 192 5 215 8',
    intro: 'Hier entstehen die gängigen Herausforderungen – z. B. widersprechende Erwartungen im Beruf. Inhalt folgt.',
  },
  {
    id: 'erleben',
    href: '/erleben',
    nav: 'Erleben',
    label: 'Erleben: Wie Glück gestalten',
    overline: 'Teil 3',
    image: '/bilder/3-erleben.svg',
    imageAnim: '/bilder/3-erleben.svg',
    alt: 'Gelbe Silhouette der sitzenden Person – das nicht greifbare Erleben',
    strich: 'M 5 8 C 38 4 84 11 122 6 C 158 2 194 9 215 6',
    intro: 'Hier entstehen Effekte und Tools im Gestalten von Erleben (Hypnosystemik). Inhalt folgt.',
  },
];
