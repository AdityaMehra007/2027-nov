import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4071, proxy: { '/api': 'http://localhost:9071' } } });
