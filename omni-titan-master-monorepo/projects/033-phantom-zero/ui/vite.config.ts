import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4033, proxy: { '/api': 'http://localhost:9033' } } });
