import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4093, proxy: { '/api': 'http://localhost:9093' } } });
