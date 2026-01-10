import { useState, useEffect } from 'react'
import { ModernTaskCard } from './ModernTaskCard'
import ModernTaskFilter from './ModernTaskFilter'
import EditTaskModal from './EditTaskModal'

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: () => void;
}

export default function ModernTaskList({ tasks, onTaskUpdate }: TaskListProps) {
  const [filters, setFilters] = useState({
    status: 'all' as 'all' | 'pending' | 'completed',
    sort: 'created' as 'created' | 'title',
    order: 'desc' as 'asc' | 'desc'
  })
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);

  // Listen for edit task events
  useEffect(() => {
    const handleEditTask = (e: Event) => {
      const customEvent = e as CustomEvent<Task>;
      setEditingTask(customEvent.detail);
      setShowEditModal(true);
    };

    window.addEventListener('editTaskRequested', handleEditTask as EventListener);
    return () => {
      window.removeEventListener('editTaskRequested', handleEditTask as EventListener);
    };
  }, []);

  const applyFilters = () => {
    let filteredTasks = [...tasks]

    // Apply status filter
    if (filters.status !== 'all') {
      if (filters.status === 'pending') {
        filteredTasks = filteredTasks.filter(task => !task.completed)
      } else if (filters.status === 'completed') {
        filteredTasks = filteredTasks.filter(task => task.completed)
      }
    }

    // Apply sorting
    filteredTasks.sort((a, b) => {
      let aValue, bValue

      if (filters.sort === 'title') {
        aValue = a.title.toLowerCase()
        bValue = b.title.toLowerCase()
      } else {
        // Sort by created date
        aValue = new Date(a.created_at).getTime()
        bValue = new Date(b.created_at).getTime()
      }

      if (filters.order === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })

    return filteredTasks
  }

  const handleFilterChange = (status: 'all' | 'pending' | 'completed', sort: 'created' | 'title', order: 'asc' | 'desc') => {
    setFilters({ status, sort, order })
  }

  const handleCloseEditModal = () => {
    setShowEditModal(false);
    setEditingTask(null);
  }

  const filteredTasks = applyFilters()

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-200">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
          <p className="text-sm text-gray-600">
            {filteredTasks.length} {filteredTasks.length === 1 ? 'task' : 'tasks'}
            {filters.status !== 'all' && ` • ${filters.status}`}
          </p>
        </div>
      </div>

      <ModernTaskFilter onFilterChange={handleFilterChange} />

      <div className="flex-1 overflow-y-auto">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-1">
              {tasks.length === 0 ? 'No tasks yet' : 'No tasks match the current filters'}
            </h3>
            <p className="text-gray-500 mb-6">
              {tasks.length === 0
                ? 'Get started by creating your first task!'
                : 'Try changing your filters to see more tasks.'}
            </p>
            {tasks.length === 0 && (
              <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Create your first task
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map((task) => (
              <ModernTaskCard key={task.id} task={task} onTaskUpdate={onTaskUpdate} />
            ))}
          </div>
        )}
      </div>

      {/* Edit Task Modal */}
      <EditTaskModal
        isOpen={showEditModal}
        onClose={handleCloseEditModal}
        task={editingTask}
        onTaskUpdated={onTaskUpdate}
      />
    </div>
  )
}