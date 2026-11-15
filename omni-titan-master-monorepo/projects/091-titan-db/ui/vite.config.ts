import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4091, proxy: { '/api': 'http://localhost:9091' } } });
