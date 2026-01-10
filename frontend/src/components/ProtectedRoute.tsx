'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface ProtectedRouteProps {
  children: React.ReactNode;
  isAuthenticated: boolean;
}

export default function ProtectedRoute({ children, isAuthenticated }: ProtectedRouteProps) {
  const router = useRouter()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p>Redirecting to login...</p>
      </div>
    )
  }

  return <>{children}</>
}