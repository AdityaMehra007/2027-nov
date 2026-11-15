import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4105, proxy: { '/api': 'http://localhost:9105' } } });
