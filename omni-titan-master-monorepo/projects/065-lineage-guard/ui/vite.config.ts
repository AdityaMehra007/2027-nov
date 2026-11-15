import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4065, proxy: { '/api': 'http://localhost:9065' } } });
