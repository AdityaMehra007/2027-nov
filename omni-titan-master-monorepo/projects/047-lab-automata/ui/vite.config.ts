import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4047, proxy: { '/api': 'http://localhost:9047' } } });
