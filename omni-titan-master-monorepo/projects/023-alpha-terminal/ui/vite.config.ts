import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4023, proxy: { '/api': 'http://localhost:9023' } } });
