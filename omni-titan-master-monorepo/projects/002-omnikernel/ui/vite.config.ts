import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4002, proxy: { '/api': 'http://localhost:9002' } } });
