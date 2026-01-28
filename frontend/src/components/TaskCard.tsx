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

export function TaskCard({ task, onTaskUpdate }: TaskCardProps) {
  const [isDeleting, setIsDeleting] = useState(false)

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

  return (
    <li className="px-3 py-3 sm:px-4 sm:py-4 hover:bg-gray-50">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-0">
        <div className="flex items-start sm:items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 mt-0.5 sm:mt-0"
          />
          <div className="ml-2 sm:ml-3 min-w-0 flex-1">
            <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </p>
            {task.description && (
              <p className="text-sm text-gray-500 truncate mt-1">{task.description}</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2 mt-2 sm:mt-0">
          <button
            onClick={handleEdit}
            className="inline-flex items-center px-2 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="inline-flex items-center px-2 py-1 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
      <div className="mt-2 flex flex-col sm:flex-row sm:justify-between gap-1 sm:gap-0">
        <div className="flex">
          <p className="flex items-center text-xs text-gray-500">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex items-center text-xs text-gray-500">
          <p>
            {task.completed ? (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Completed
              </span>
            ) : (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Pending
              </span>
            )}
          </p>
        </div>
      </div>
    </li>
  )
}