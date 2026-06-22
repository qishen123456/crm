import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { login as apiLogin, me as apiMe, switchRole as apiSwitchRole, type AuthUser } from '../api/auth'

interface AuthState {
  token: string | null
  user: AuthUser | null
  isAuthenticated: boolean
  isLoading: boolean
  isRolePreview: boolean
  setToken: (token: string | null) => void
  setUser: (user: AuthUser | null) => void
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  restore: () => Promise<boolean>
  switchRole: (roleCode: string) => Promise<void>
  hasPermission: (code: string) => boolean
}

const STORAGE_KEY = 'angelcrm_auth'

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      isRolePreview: false,

      setToken: (token) => set({ token }),
      setUser: (user) => set({ user, isAuthenticated: !!user }),

      login: async (email, password) => {
        const res = await apiLogin(email, password)
        set({ token: res.access_token, user: res.user, isAuthenticated: true, isRolePreview: false })
      },

      logout: () => {
        set({ token: null, user: null, isAuthenticated: false, isRolePreview: false })
        localStorage.removeItem(STORAGE_KEY)
      },

      restore: async () => {
        const { token } = get()
        if (!token) return false
        set({ isLoading: true })
        try {
          const user = await apiMe()
          set({ user, isAuthenticated: true, isLoading: false })
          return true
        } catch (e) {
          set({ token: null, user: null, isAuthenticated: false, isLoading: false })
          return false
        }
      },

      switchRole: async (roleCode) => {
        const res = await apiSwitchRole(roleCode)
        set({ token: res.access_token, user: res.user, isAuthenticated: true, isRolePreview: true })
      },

      hasPermission: (code) => {
        const { user } = get()
        if (!user) return false
        return user.permissions.includes(code)
      },
    }),
    {
      name: STORAGE_KEY,
      partialize: (state) => ({ token: state.token, isRolePreview: state.isRolePreview }),
    }
  )
)
