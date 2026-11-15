import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4016, proxy: { '/api': 'http://localhost:9016' } } });
