import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4041, proxy: { '/api': 'http://localhost:9041' } } });
