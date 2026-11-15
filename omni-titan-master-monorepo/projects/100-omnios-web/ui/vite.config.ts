import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4100, proxy: { '/api': 'http://localhost:9100' } } });
