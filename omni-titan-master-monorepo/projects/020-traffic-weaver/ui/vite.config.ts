import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4020, proxy: { '/api': 'http://localhost:9020' } } });
