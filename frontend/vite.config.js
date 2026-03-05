import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path";
import fs from 'fs';
import manifest from './public/manifest.js'
// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // 自定义插件：自动同步生成 manifest.json
    {
      name: 'generate-manifest',
      closeBundle() {
        const distPath = path.resolve(__dirname, 'dist/manifest.json');
        fs.writeFileSync(distPath, JSON.stringify(manifest, null, 2));
        console.log('已从 manifest.js 同步配置至 dist/manifest.json');
      }
    }
  ],
  base: './',
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    }
  },
  build: {
    outDir: 'dist', // 打包输出目录
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'), // 侧边栏入口
        content: path.resolve(__dirname, 'src/content/index.js'),
        background: path.resolve(__dirname, 'public/background.js'),
      },
    output: {
        assetFileNames: 'assets/[name].[ext]',
        chunkFileNames: 'assets/[name].js',
        entryFileNames: 'assets/[name].js',
      },
    },
  },

})
