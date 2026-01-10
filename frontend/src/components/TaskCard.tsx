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
    <li className="px-4 py-4 sm:px-6 hover:bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
          />
          <div className="ml-3 min-w-0 flex-1">
            <p className={`text-sm font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </p>
            {task.description && (
              <p className="text-sm text-gray-500 truncate">{task.description}</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleEdit}
            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
      <div className="mt-2 sm:flex sm:justify-between">
        <div className="sm:flex">
          <p className="flex items-center text-xs text-gray-500">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="mt-2 flex items-center text-xs text-gray-500 sm:mt-0">
          <p>
            {task.completed ? (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Completed
              </span>
            ) : (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Pending
              </span>
            )}
          </p>
        </div>
      </div>
    </li>
  )
}