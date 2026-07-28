// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build
export default defineConfig({
  // Live-Domain (für saubere Canonical-/OG-URLs).
  site: 'https://psychenow.netlify.app',
  // Statische Ausgabe -> nach Netlify (publish = site/dist).
  output: 'static',
});
