import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4101, proxy: { '/api': 'http://localhost:9101' } } });
