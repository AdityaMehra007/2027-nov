import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4034, proxy: { '/api': 'http://localhost:9034' } } });
