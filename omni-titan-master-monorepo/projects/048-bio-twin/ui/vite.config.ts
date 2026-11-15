import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4048, proxy: { '/api': 'http://localhost:9048' } } });
