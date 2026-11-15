import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4031, proxy: { '/api': 'http://localhost:9031' } } });
