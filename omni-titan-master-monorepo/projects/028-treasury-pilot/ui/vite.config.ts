import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4028, proxy: { '/api': 'http://localhost:9028' } } });
