import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
      '/healthz': 'http://localhost:8000',
      '/metrics': 'http://localhost:8000'
    }
  }
});
