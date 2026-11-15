import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4029, proxy: { '/api': 'http://localhost:9029' } } });
