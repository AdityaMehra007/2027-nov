import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4050, proxy: { '/api': 'http://localhost:9050' } } });
