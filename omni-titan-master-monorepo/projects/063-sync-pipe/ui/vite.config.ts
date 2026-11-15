import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4063, proxy: { '/api': 'http://localhost:9063' } } });
