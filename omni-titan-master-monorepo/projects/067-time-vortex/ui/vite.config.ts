import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4067, proxy: { '/api': 'http://localhost:9067' } } });
