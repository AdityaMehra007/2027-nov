import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4007, proxy: { '/api': 'http://localhost:9007' } } });
