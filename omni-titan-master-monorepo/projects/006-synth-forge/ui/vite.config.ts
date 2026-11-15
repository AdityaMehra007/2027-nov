import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4006, proxy: { '/api': 'http://localhost:9006' } } });
