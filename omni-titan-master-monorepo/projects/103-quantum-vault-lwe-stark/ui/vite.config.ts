import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4103, proxy: { '/api': 'http://localhost:9103' } } });
