import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4046, proxy: { '/api': 'http://localhost:9046' } } });
