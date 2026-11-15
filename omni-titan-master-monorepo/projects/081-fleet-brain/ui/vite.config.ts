import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4081, proxy: { '/api': 'http://localhost:9081' } } });
