import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4030, proxy: { '/api': 'http://localhost:9030' } } });
