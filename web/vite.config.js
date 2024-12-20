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
    port: 7070,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://192.168.6.93:4080',
        changeOrigin: true,
        //rewrite: (path) => path.replace(/^\/api/, ''), // 去掉 `/api` 前缀
      },
    },
  },
});