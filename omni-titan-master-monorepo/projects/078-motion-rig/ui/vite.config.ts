import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4078, proxy: { '/api': 'http://localhost:9078' } } });
