import { useState } from 'react'

interface TaskFilterProps {
  onFilterChange: (status: 'all' | 'pending' | 'completed', sort: 'created' | 'title', order: 'asc' | 'desc') => void;
}

export default function ModernTaskFilter({ onFilterChange }: TaskFilterProps) {
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
    <div className="flex flex-wrap gap-4 mb-6 p-4 bg-white rounded-xl shadow-sm border border-gray-100">
      {/* Status Filters */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => handleStatusChange('all')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all duration-200 ${
            status === 'all'
              ? 'bg-indigo-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
            </svg>
            All
          </div>
        </button>

        <button
          onClick={() => handleStatusChange('pending')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all duration-200 ${
            status === 'pending'
              ? 'bg-yellow-500 text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
            </svg>
            Pending
          </div>
        </button>

        <button
          onClick={() => handleStatusChange('completed')}
          className={`px-4 py-2 text-sm rounded-lg font-medium transition-all duration-200 ${
            status === 'completed'
              ? 'bg-green-500 text-white shadow-md'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Completed
          </div>
        </button>
      </div>

      {/* Sort Controls */}
      <div className="flex flex-wrap gap-2">
        <div className="flex items-center bg-gray-100 rounded-lg px-3 py-2">
          <label className="text-sm font-medium text-gray-700 mr-2">Sort by:</label>
          <select
            value={sort}
            onChange={(e) => handleSortChange(e.target.value as 'created' | 'title')}
            className="bg-transparent border-0 text-sm focus:ring-0 focus:outline-none"
          >
            <option value="created">Created Date</option>
            <option value="title">Title</option>
          </select>
        </div>

        <div className="flex items-center bg-gray-100 rounded-lg px-3 py-2">
          <label className="text-sm font-medium text-gray-700 mr-2">Order:</label>
          <select
            value={order}
            onChange={(e) => handleOrderChange(e.target.value as 'asc' | 'desc')}
            className="bg-transparent border-0 text-sm focus:ring-0 focus:outline-none"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>
      </div>
    </div>
  )
}