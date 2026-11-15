import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4062, proxy: { '/api': 'http://localhost:9062' } } });
