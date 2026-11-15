import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4069, proxy: { '/api': 'http://localhost:9069' } } });
