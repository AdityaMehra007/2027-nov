import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4025, proxy: { '/api': 'http://localhost:9025' } } });
