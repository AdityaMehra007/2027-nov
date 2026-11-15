import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4073, proxy: { '/api': 'http://localhost:9073' } } });
