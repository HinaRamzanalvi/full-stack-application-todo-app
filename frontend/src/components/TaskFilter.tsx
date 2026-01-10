import { useState } from 'react'

interface TaskFilterProps {
  onFilterChange: (status: 'all' | 'pending' | 'completed', sort: 'created' | 'title', order: 'asc' | 'desc') => void;
}

export default function TaskFilter({ onFilterChange }: TaskFilterProps) {
  const [status, setStatus] = useState<'all' | 'pending' | 'completed'>('all')
  const [sort, setSort] = useState<'created' | 'title'>('created')
  const [order, setOrder] = useState<'asc' | 'desc'>('desc')

  const handleStatusChange = (newStatus: 'all' | 'pending' | 'completed') => {
    setStatus(newStatus)
    onFilterChange(newStatus, sort, order)
  }

  const handleSortChange = (newSort: 'created' | 'title') => {
    setSort(newSort)
    onFilterChange(status, newSort, order)
  }

  const handleOrderChange = (newOrder: 'asc' | 'desc') => {
    setOrder(newOrder)
    onFilterChange(status, sort, newOrder)
  }

  return (
    <div className="flex flex-wrap gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
      <div className="flex items-center space-x-2">
        <label className="text-sm font-medium text-gray-700">Status:</label>
        <div className="flex space-x-2">
          <button
            onClick={() => handleStatusChange('all')}
            className={`px-3 py-1 text-sm rounded-md ${
              status === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => handleStatusChange('pending')}
            className={`px-3 py-1 text-sm rounded-md ${
              status === 'pending'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => handleStatusChange('completed')}
            className={`px-3 py-1 text-sm rounded-md ${
              status === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Completed
          </button>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <label className="text-sm font-medium text-gray-700">Sort by:</label>
        <select
          value={sort}
          onChange={(e) => handleSortChange(e.target.value as 'created' | 'title')}
          className="border border-gray-300 rounded-md px-3 py-1 text-sm"
        >
          <option value="created">Created Date</option>
          <option value="title">Title</option>
        </select>
      </div>

      <div className="flex items-center space-x-2">
        <label className="text-sm font-medium text-gray-700">Order:</label>
        <select
          value={order}
          onChange={(e) => handleOrderChange(e.target.value as 'asc' | 'desc')}
          className="border border-gray-300 rounded-md px-3 py-1 text-sm"
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>
    </div>
  )
}