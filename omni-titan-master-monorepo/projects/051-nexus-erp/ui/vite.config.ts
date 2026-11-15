import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4051, proxy: { '/api': 'http://localhost:9051' } } });
