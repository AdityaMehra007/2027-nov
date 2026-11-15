import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4086, proxy: { '/api': 'http://localhost:9086' } } });
