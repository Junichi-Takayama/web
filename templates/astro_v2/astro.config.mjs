import { defineConfig } from 'astro/config';

import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://example.com',
  output: 'static',
  server: {
    port: 4322,
  },
  integrations: [tailwind()],
});