import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4094, proxy: { '/api': 'http://localhost:9094' } } });
