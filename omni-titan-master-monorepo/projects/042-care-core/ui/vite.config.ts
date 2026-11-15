import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4042, proxy: { '/api': 'http://localhost:9042' } } });
