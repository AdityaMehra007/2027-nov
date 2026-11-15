import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4057, proxy: { '/api': 'http://localhost:9057' } } });
