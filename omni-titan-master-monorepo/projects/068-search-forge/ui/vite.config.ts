import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4068, proxy: { '/api': 'http://localhost:9068' } } });
