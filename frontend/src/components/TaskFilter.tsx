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
    <div className="flex flex-wrap gap-3 md:gap-4 mb-3 md:mb-4 p-3 md:p-4 bg-gray-50 rounded-lg">
      <div className="flex flex-col sm:flex-row sm:items-center gap-2">
        <label className="text-xs sm:text-sm font-medium text-gray-700 whitespace-nowrap">Status:</label>
        <div className="flex flex-wrap gap-1">
          <button
            onClick={() => handleStatusChange('all')}
            className={`px-2.5 py-1 text-xs sm:px-3 sm:py-1 sm:text-sm rounded-md ${
              status === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => handleStatusChange('pending')}
            className={`px-2.5 py-1 text-xs sm:px-3 sm:py-1 sm:text-sm rounded-md ${
              status === 'pending'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => handleStatusChange('completed')}
            className={`px-2.5 py-1 text-xs sm:px-3 sm:py-1 sm:text-sm rounded-md ${
              status === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 border border-gray-300'
            }`}
          >
            Completed
          </button>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center gap-2">
        <label className="text-xs sm:text-sm font-medium text-gray-700 whitespace-nowrap">Sort by:</label>
        <select
          value={sort}
          onChange={(e) => handleSortChange(e.target.value as 'created' | 'title')}
          className="border border-gray-300 rounded-md px-2.5 py-1 text-xs sm:px-3 sm:py-1 sm:text-sm"
        >
          <option value="created">Created Date</option>
          <option value="title">Title</option>
        </select>
      </div>

      <div className="flex flex-col sm:flex-row sm:items-center gap-2">
        <label className="text-xs sm:text-sm font-medium text-gray-700 whitespace-nowrap">Order:</label>
        <select
          value={order}
          onChange={(e) => handleOrderChange(e.target.value as 'asc' | 'desc')}
          className="border border-gray-300 rounded-md px-2.5 py-1 text-xs sm:px-3 sm:py-1 sm:text-sm"
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>
    </div>
  )
}