import { defineConfig } from 'vite';
import path from 'path';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 4081,
    cors: true,
    proxy: {
      '/rest': {
        target: process.env.VITE_API_ENDPOINT,
        changeOrigin: true,
        //rewrite: (path) => path.replace(/^\/api/, ''), // 去掉 `/api` 前缀
      },
    },
  },
});