import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4104, proxy: { '/api': 'http://localhost:9104' } } });
