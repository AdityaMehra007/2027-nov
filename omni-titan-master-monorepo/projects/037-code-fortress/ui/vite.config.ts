import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4037, proxy: { '/api': 'http://localhost:9037' } } });
