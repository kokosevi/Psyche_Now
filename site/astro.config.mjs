// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build
export default defineConfig({
  // Beim Live-Gang hier die echte Netlify-URL eintragen (für saubere Canonical-/OG-URLs).
  site: 'https://psyche-now.example',
  // Statische Ausgabe -> nach Netlify (publish = site/dist).
  output: 'static',
});
