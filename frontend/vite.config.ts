import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    chunkSizeWarningLimit: 1500,
    rollupOptions: {
      output: {
        manualChunks(id: string | undefined) {
          if (!id) return
          if (id.includes('node_modules')) {
            if (id.includes('antd') || id.includes('@ant-design')) return 'antd'
            if (id.includes('echarts')) return 'echarts'
            if (id.includes('react') || id.includes('react-dom') || id.includes('react-router')) return 'react'
            return 'vendor'
          }
        },
      },
    },
  },
})
