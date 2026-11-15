import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4038, proxy: { '/api': 'http://localhost:9038' } } });
