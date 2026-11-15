import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4027, proxy: { '/api': 'http://localhost:9027' } } });
