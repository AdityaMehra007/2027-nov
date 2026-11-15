import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4108, proxy: { '/api': 'http://localhost:9108' } } });
