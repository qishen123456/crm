import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/useAuthStore'

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, token, restore, isLoading } = useAuthStore()
  const [hydrated, setHydrated] = useState(false)
  const [restored, setRestored] = useState(false)

  useEffect(() => {
    // Wait for Zustand persist to rehydrate the token from localStorage
    const finish = () => setHydrated(true)
    const unsubscribe = useAuthStore.persist.onFinishHydration(finish)
    if (useAuthStore.persist.hasHydrated()) {
      finish()
    }
    return () => unsubscribe()
  }, [])

  useEffect(() => {
    if (!hydrated) return
    if (token && !isAuthenticated) {
      restore().finally(() => setRestored(true))
    } else {
      setRestored(true)
    }
  }, [hydrated, token, isAuthenticated, restore])

  if (!hydrated || !restored || isLoading) {
    return <div style={{ height: '100vh' }} />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
