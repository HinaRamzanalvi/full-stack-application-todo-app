import { useState } from 'react'
import { apiClient } from '@/lib/api'

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

interface TaskCardProps {
  task: Task;
  onTaskUpdate: () => void;
}

export function ModernTaskCard({ task, onTaskUpdate }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const handleToggleCompletion = async () => {
    try {
      await apiClient.toggleTaskCompletion(task.id)
      onTaskUpdate()
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return

    try {
      setIsDeleting(true)
      await apiClient.deleteTask(task.id)
      onTaskUpdate()
    } catch (error) {
      console.error('Failed to delete task:', error)
      setIsDeleting(false)
    }
  }

  const handleEdit = () => {
    // Emit a custom event to trigger the edit modal in the parent component
    window.dispatchEvent(new CustomEvent('editTaskRequested', { detail: task }));
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div
      className={`bg-white/70 backdrop-blur-sm rounded-xl border transition-all duration-300 hover:shadow-lg p-4 mb-3 relative overflow-hidden ${
        task.completed
          ? 'border-green-200/50 bg-green-50/30'
          : 'border-gray-200/50 hover:border-indigo-200/50'
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={`absolute inset-0 bg-gradient-to-r ${task.completed ? 'from-green-50/30 to-emerald-50/30' : 'from-indigo-50/20 to-purple-50/20'} opacity-30 pointer-events-none`}></div>
      <div className="relative z-10">
      <div className="flex items-start space-x-3">
        <button
          onClick={handleToggleCompletion}
          className={`flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5 transition-all duration-200 ${
            task.completed
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-gray-400 hover:border-indigo-500'
          }`}
          aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {task.completed && (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0">
          <h3 className={`text-base font-medium ${
            task.completed
              ? 'text-gray-500 line-through'
              : 'text-gray-800'
          }`}>
            {task.title}
          </h3>

          {task.description && (
            <p className={`mt-1 text-sm ${
              task.completed
                ? 'text-gray-400'
                : 'text-gray-600'
            }`}>
              {task.description}
            </p>
          )}

          <div className="mt-3 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                task.completed
                  ? 'bg-green-100 text-green-800'
                  : 'bg-indigo-100 text-indigo-800'
              }`}>
                {task.completed ? (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Done
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                    Pending
                  </>
                )}
              </span>

              <span className="text-xs text-gray-500">
                {formatDate(task.created_at)}
              </span>
            </div>

            {(isHovered || isDeleting) && (
              <div className="flex space-x-1.5">
                <button
                  onClick={handleEdit}
                  className="flex-shrink-0 inline-flex items-center px-2.5 py-1 border border-transparent text-xs font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 transition-colors"
                  title="Edit task"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                </button>
                <button
                  onClick={handleDelete}
                  disabled={isDeleting}
                  className="flex-shrink-0 inline-flex items-center px-2.5 py-1 border border-transparent text-xs font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 transition-colors"
                  title="Delete task"
                >
                  {isDeleting ? (
                    <svg className="animate-spin h-3.5 w-3.5 text-red-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2 9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      </div>
    </div>
  )
}