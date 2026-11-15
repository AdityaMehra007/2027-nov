import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4049, proxy: { '/api': 'http://localhost:9049' } } });
