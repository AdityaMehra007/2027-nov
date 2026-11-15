import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4072, proxy: { '/api': 'http://localhost:9072' } } });
