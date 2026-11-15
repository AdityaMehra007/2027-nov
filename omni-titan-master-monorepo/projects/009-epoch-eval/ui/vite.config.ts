import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4009, proxy: { '/api': 'http://localhost:9009' } } });
