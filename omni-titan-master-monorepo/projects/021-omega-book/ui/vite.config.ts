import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4021, proxy: { '/api': 'http://localhost:9021' } } });
