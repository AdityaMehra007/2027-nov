import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4013, proxy: { '/api': 'http://localhost:9013' } } });
