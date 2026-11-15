import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4040, proxy: { '/api': 'http://localhost:9040' } } });
