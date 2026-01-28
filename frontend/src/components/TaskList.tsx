import { useState, useEffect } from 'react'
import { TaskCard } from './TaskCard'
import TaskFilter from './TaskFilter'
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

export default function TaskList({ tasks, onTaskUpdate }: TaskListProps) {
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
    <>
      <TaskFilter onFilterChange={handleFilterChange} />
      <ul className="divide-y divide-gray-200">
        {filteredTasks.length === 0 ? (
          <li className="px-3 py-3 sm:px-4 sm:py-4">
            <p className="text-gray-500 text-center text-sm">
              {tasks.length === 0
                ? 'No tasks yet. Create your first task!'
                : 'No tasks match the current filters.'}
            </p>
          </li>
        ) : (
          filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} onTaskUpdate={onTaskUpdate} />
          ))
        )}
      </ul>

      {/* Edit Task Modal */}
      <EditTaskModal
        isOpen={showEditModal}
        onClose={handleCloseEditModal}
        task={editingTask}
        onTaskUpdated={onTaskUpdate}
      />
    </>
  )
}