import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4087, proxy: { '/api': 'http://localhost:9087' } } });
