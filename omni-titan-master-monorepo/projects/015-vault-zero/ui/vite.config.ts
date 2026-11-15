import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4015, proxy: { '/api': 'http://localhost:9015' } } });
