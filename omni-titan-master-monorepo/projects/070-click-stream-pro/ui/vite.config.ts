import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4070, proxy: { '/api': 'http://localhost:9070' } } });
