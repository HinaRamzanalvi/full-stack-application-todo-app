'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(true)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  // Check if user is logged in
  useEffect(() => {
    // In a real app, you would check for auth tokens here
    // For now, we'll just redirect to login
    setIsLoading(false)
    setIsLoggedIn(false)
  }, [])

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-teal-50 p-4 relative overflow-hidden">
      {/* Background pattern overlay for subtle texture */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}></div>
      </div>

      {/* Floating abstract shapes */}
      <div className="absolute top-20 left-10 w-32 h-32 rounded-full bg-blue-200/30 blur-xl hidden md:block"></div>
      <div className="absolute bottom-20 right-10 w-40 h-40 rounded-full bg-purple-200/30 blur-xl hidden md:block"></div>
      <div className="absolute top-1/3 right-1/4 w-24 h-24 rounded-full bg-teal-200/30 blur-xl hidden md:block"></div>

      <div className="w-full max-w-2xl z-10">
        <div className="text-center mb-8 md:mb-10">
          <div className="mx-auto w-16 h-16 md:w-20 md:h-20 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg mb-4 md:mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 md:h-10 md:w-10 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <path d="M16 13H8" />
              <path d="M16 17H8" />
              <path d="M10 9H8" />
            </svg>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-teal-600 bg-clip-text text-transparent mb-3 md:mb-4">
            Welcome to Hackathon II Todo App
          </h1>
          <p className="text-base md:text-lg lg:text-xl text-gray-700 max-w-xs sm:max-w-md mx-auto">
            A secure, multi-user todo application
          </p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl md:rounded-3xl shadow-xl md:shadow-2xl border border-white/30 p-6 md:p-8 lg:p-12">
          <div className="text-center mb-6 md:mb-10">
            <h2 className="text-xl md:text-2xl font-semibold text-gray-900 mb-2">Get Started Today</h2>
            <p className="text-sm md:text-base text-gray-600">Join thousands of users who organize their tasks efficiently</p>
          </div>

          <div className="space-y-4 md:space-y-5">
            <div>
              <Link href="/login">
                <button
                  type="button"
                  className="w-full flex justify-center py-3 px-4 md:py-4 md:px-6 border border-transparent rounded-lg md:rounded-xl shadow-md md:shadow-lg text-sm md:text-base font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 md:focus:ring-4 focus:ring-blue-300/50 transition-all duration-300 transform hover:scale-[1.02]"
                >
                  Sign in to your account
                </button>
              </Link>
            </div>

            <div className="pt-3 md:pt-4">
              <Link href="/signup">
                <button
                  type="button"
                  className="w-full flex justify-center py-3 px-4 md:py-4 md:px-6 border border-gray-300 rounded-lg md:rounded-xl shadow-md md:shadow-lg text-sm md:text-base font-medium text-gray-800 bg-gradient-to-r from-white to-gray-100 hover:from-gray-50 hover:to-gray-200 focus:outline-none focus:ring-2 md:focus:ring-4 focus:ring-gray-300/50 transition-all duration-300 transform hover:scale-[1.02]"
                >
                  Create new account
                </button>
              </Link>
            </div>
          </div>
        </div>

        <div className="text-center mt-6 md:mt-8">
          <p className="text-xs text-gray-500">
            © {new Date().getFullYear()} Hackathon II Todo App. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  )
}