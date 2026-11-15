import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4010, proxy: { '/api': 'http://localhost:9010' } } });
