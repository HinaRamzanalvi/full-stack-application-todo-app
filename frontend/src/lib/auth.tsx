'use client'

import { useState, useEffect, createContext, useContext, ReactNode } from 'react'
import { apiClient } from './api'

interface User {
  id: string;
  email: string;
  name?: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  resetSession: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing session on component mount
    checkSession()
  }, [])

  const checkSession = async () => {
    // Check for token in localStorage and validate it
    const token = localStorage.getItem('token')
    if (token) {
      // Set the token in the API client
      apiClient.setToken(token)

      // Try to validate the token by fetching user info from the backend
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        })

        if (response.ok) {
          const userData = await response.json()
          // Store user data for future use
          localStorage.setItem('user', JSON.stringify(userData))
          setUser(userData)
        } else {
          // Token is invalid, clear it
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          apiClient.setToken('')
        }
      } catch (error) {
        console.error('Error validating session with backend:', error)
        // Clear potentially invalid token
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        apiClient.setToken('')
      }
    }
    setLoading(false)
  }

  const login = async (email: string, password: string) => {
    try {
      // Make API call to login using apiClient
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        // Get error details from response
        let errorMessage = 'Login failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          // If we can't parse the error response, use the status text
          errorMessage = `Login failed: ${response.status} ${response.statusText}`;
        }

        console.error('Login error:', errorMessage);
        throw new Error(errorMessage);
      }

      const data: LoginResponse = await response.json()

      // Store the token and user info
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))

      // Set the token in the API client
      apiClient.setToken(data.access_token)

      setUser(data.user)
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const signup = async (name: string, email: string, password: string) => {
    try {
      // Make API call to register
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      })

      if (!response.ok) {
        // Get error details from response
        let errorMessage = 'Signup failed';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (e) {
          // If we can't parse the error response, use the status text
          errorMessage = `Signup failed: ${response.status} ${response.statusText}`;
        }

        console.error('Signup error:', errorMessage);
        throw new Error(errorMessage);
      }

      const userData: User = await response.json()

      // Automatically login after successful signup
      await login(email, password)
    } catch (error) {
      console.error('Signup error:', error)
      throw error
    }
  }

  const logout = () => {
    // Remove token and user from localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    // Clear token from API client
    apiClient.setToken('')

    setUser(null)
  }

  const resetSession = () => {
    // Clear all auth-related data to reset the session
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    // Clear token from API client
    apiClient.setToken('')

    // Reset user state
    setUser(null)

    // Re-check session to ensure proper state
    setTimeout(() => {
      checkSession()
    }, 100)
  }

  const value: AuthContextType = {
    user,
    loading,
    login,
    signup,
    logout,
    resetSession,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}