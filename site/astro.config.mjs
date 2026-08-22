// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build
export default defineConfig({
  // Live-Domain (für saubere Canonical-/OG-URLs).
  site: 'https://feelright.ch',
  // Statische Ausgabe -> nach Netlify (publish = site/dist).
  output: 'static',
});
