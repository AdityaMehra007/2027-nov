import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4011, proxy: { '/api': 'http://localhost:9011' } } });
