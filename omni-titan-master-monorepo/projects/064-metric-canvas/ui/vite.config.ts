import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4064, proxy: { '/api': 'http://localhost:9064' } } });
