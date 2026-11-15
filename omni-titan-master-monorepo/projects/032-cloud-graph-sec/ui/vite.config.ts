import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4032, proxy: { '/api': 'http://localhost:9032' } } });
