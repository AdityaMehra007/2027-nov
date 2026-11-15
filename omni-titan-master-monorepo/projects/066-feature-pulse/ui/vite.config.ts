import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4066, proxy: { '/api': 'http://localhost:9066' } } });
