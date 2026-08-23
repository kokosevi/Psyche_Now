import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['src/**/*.test.ts'],
    environment: 'node',
    // index.test.ts baut die Site einmalig (astro build) und prüft dist/.
    testTimeout: 120_000,
    hookTimeout: 120_000,
  },
});
