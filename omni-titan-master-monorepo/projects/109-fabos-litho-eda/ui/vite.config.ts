import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4109, proxy: { '/api': 'http://localhost:9109' } } });
