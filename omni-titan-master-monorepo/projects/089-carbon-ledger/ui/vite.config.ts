import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4089, proxy: { '/api': 'http://localhost:9089' } } });
