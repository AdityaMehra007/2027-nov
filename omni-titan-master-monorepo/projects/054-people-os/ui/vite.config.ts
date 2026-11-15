import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4054, proxy: { '/api': 'http://localhost:9054' } } });
