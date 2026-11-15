import { defineConfig } from 'vite';
export default defineConfig({ server: { port: 4077, proxy: { '/api': 'http://localhost:9077' } } });
