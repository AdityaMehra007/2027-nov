import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4112, proxy: { '/api': 'http://localhost:9112' } } });
