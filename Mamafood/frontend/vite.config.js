import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
  build: {
    sourcemap: true, // Enable source maps
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src',  // Alias für das src-Verzeichnis
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/assets/_variables.scss" as *;`
      }
    }
  }
})

