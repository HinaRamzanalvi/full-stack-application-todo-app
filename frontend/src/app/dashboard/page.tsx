'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { apiClient } from '@/lib/api'
import ModernTaskList from '@/components/ModernTaskList'
import ModernCreateTaskForm from '@/components/ModernCreateTaskForm'
import ModernHeader from '@/components/ModernHeader'
import FloatingChatBot from '@/components/FloatingChatBot'

export default function DashboardPage() {
  const [tasks, setTasks] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const { isAuthenticated, loading: authLoading } = useAuth()
  const router = useRouter()

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, authLoading, router])

  // Load tasks when component mounts
  useEffect(() => {
    if (isAuthenticated) {
      loadTasks()
    }
  }, [isAuthenticated])

  const loadTasks = async () => {
    try {
      setLoading(true)
      const response = await apiClient.getTasks()
      setTasks(response.tasks || response)
    } catch (error) {
      console.error('Failed to load tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTaskCreated = (newTask: any) => {
    // Refresh the task list to get the latest from the backend
    loadTasks()
  }

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-gray-600 font-medium">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50">
      <ModernHeader />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 md:py-6">
        <div className="flex flex-col md:flex-row gap-4 md:gap-6 h-auto md:h-[calc(100vh-120px)]">
          {/* Sidebar - Mobile first approach with collapsible sidebar */}
          <div className="w-full md:w-72 lg:w-80 flex-shrink-0 order-2 md:order-1">
            <div className="bg-white/80 backdrop-blur-sm rounded-xl md:rounded-2xl shadow-lg md:shadow-xl border border-white/20 overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 opacity-60 pointer-events-none"></div>
              <div className="relative z-10 p-4 md:p-6">
                <div className="mb-4 md:mb-6">
                  <h2 className="text-xl md:text-2xl font-bold text-gray-800 mb-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 md:h-6 md:w-6 mr-2 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                    </svg>
                    Create Task
                  </h2>
                  <p className="text-xs md:text-sm text-gray-600">Add a new task to your list</p>
                </div>

                <ModernCreateTaskForm onTaskCreated={handleTaskCreated} />

                <div className="mt-6 md:mt-8 pt-4 md:pt-6 border-t border-gray-200">
                  <h3 className="font-semibold text-gray-700 mb-3 flex items-center text-sm md:text-base">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 md:h-4 md:w-4 mr-2 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    Quick Stats
                  </h3>
                  <div className="grid grid-cols-2 gap-2 md:gap-3">
                    <div className="bg-indigo-50 rounded-lg p-2 md:p-3 text-center">
                      <div className="text-lg md:text-2xl font-bold text-indigo-700">{tasks.length}</div>
                      <div className="text-xs md:text-xs text-indigo-600">Total</div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-2 md:p-3 text-center">
                      <div className="text-lg md:text-2xl font-bold text-green-700">{tasks.filter(t => t.completed).length}</div>
                      <div className="text-xs md:text-xs text-green-600">Done</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 w-full order-1 md:order-2">
            <div className="bg-white/80 backdrop-blur-sm rounded-xl md:rounded-2xl shadow-lg md:shadow-xl border border-white/20 h-full min-h-[500px] md:min-h-[600px] overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50/30 to-indigo-50/30 opacity-40 pointer-events-none"></div>
              <div className="relative z-10 h-full">
                <div className="p-4 md:p-6 border-b border-gray-200">
                  <h2 className="text-xl md:text-2xl font-bold text-gray-800">Your Tasks</h2>
                  <p className="text-sm md:text-base text-gray-600">Manage your daily tasks and activities</p>
                </div>

                <div className="p-3 md:p-4 h-[calc(100%-60px)] md:h-[calc(100%-72px)] overflow-y-auto">
                  <ModernTaskList tasks={tasks} onTaskUpdate={loadTasks} />
                </div>
              </div>
            </div>
          </div>

          {/* Main Content and Sidebar Container */}
        </div>
      </div>

      {/* Floating ChatBot Component */}
      <FloatingChatBot />
    </div>
  )
}