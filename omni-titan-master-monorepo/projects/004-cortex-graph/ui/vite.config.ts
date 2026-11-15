import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4004, proxy: { '/api': 'http://localhost:9004' } } });
