import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4080, proxy: { '/api': 'http://localhost:9080' } } });
