import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4052, proxy: { '/api': 'http://localhost:9052' } } });
