import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4076, proxy: { '/api': 'http://localhost:9076' } } });
