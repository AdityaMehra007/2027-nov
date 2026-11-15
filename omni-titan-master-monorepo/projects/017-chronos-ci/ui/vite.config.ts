import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4017, proxy: { '/api': 'http://localhost:9017' } } });
