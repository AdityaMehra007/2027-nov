import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4092, proxy: { '/api': 'http://localhost:9092' } } });
