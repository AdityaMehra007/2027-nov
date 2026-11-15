import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4060, proxy: { '/api': 'http://localhost:9060' } } });
