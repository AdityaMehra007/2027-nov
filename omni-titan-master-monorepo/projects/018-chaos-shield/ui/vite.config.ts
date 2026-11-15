import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4018, proxy: { '/api': 'http://localhost:9018' } } });
