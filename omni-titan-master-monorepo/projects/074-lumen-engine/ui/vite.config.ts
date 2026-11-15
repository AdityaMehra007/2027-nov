import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4074, proxy: { '/api': 'http://localhost:9074' } } });
