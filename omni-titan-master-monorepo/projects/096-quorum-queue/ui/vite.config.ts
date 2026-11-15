import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4096, proxy: { '/api': 'http://localhost:9096' } } });
