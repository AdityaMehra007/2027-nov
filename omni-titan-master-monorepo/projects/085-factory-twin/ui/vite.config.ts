import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4085, proxy: { '/api': 'http://localhost:9085' } } });
