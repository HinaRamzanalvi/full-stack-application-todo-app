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

  const checkSession = () => {
    // Check for token in localStorage and validate it
    const token = localStorage.getItem('token')
    if (token) {
      // Set the token in the API client
      apiClient.setToken(token)

      // We'll use the user info from localStorage as well
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        setUser(JSON.parse(storedUser))
      }
    }
    setLoading(false)
  }

  const login = async (email: string, password: string) => {
    try {
      // Make API call to login using apiClient
      const response = await fetch(`${(apiClient as any).baseUrl}/api/auth/login`, {
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
      const response = await fetch(`${(apiClient as any).baseUrl}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      })

      if (!response.ok) {
        throw new Error('Signup failed')
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

  const value: AuthContextType = {
    user,
    loading,
    login,
    signup,
    logout,
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