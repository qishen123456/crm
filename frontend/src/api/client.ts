import axios from 'axios'
import { i18n } from '../locales'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.request.use((config) => {
  config.headers = config.headers || {}
  config.headers['Accept-Language'] = i18n.language
  return config
})

// Re-export common HTTP methods for convenience
export const api = {
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  patch: apiClient.patch,
  delete: apiClient.delete,
}
