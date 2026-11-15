import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4012, proxy: { '/api': 'http://localhost:9012' } } });
