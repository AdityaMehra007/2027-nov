import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4019, proxy: { '/api': 'http://localhost:9019' } } });
