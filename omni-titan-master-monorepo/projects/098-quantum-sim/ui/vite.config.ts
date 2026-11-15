import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4098, proxy: { '/api': 'http://localhost:9098' } } });
