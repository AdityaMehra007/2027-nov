import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4059, proxy: { '/api': 'http://localhost:9059' } } });
