import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4036, proxy: { '/api': 'http://localhost:9036' } } });
