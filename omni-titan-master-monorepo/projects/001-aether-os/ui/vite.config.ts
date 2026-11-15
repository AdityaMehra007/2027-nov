import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4001, proxy: { '/api': 'http://localhost:9001' } } });
