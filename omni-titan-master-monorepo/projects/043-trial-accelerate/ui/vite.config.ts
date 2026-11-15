import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4043, proxy: { '/api': 'http://localhost:9043' } } });
