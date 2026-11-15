import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4053, proxy: { '/api': 'http://localhost:9053' } } });
