'use client'

import { Task } from '@/types'
import { CheckCircle, Circle, Clock, Trash2 } from 'lucide-react'
import apiClient from '@/lib/api/client'
import toast from 'react-hot-toast'

interface TaskItemProps {
  task: Task
  onUpdate: () => void
}

export function TaskItem({ task, onUpdate }: TaskItemProps) {
  const priorityColors = {
    low: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    medium: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
    urgent: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
  }

  const handleToggleComplete = async () => {
    try {
      const newStatus = task.status === 'completed' ? 'pending' : 'completed'
      await apiClient.patch(`/tasks/${task.id}`, { status: newStatus })
      toast.success(newStatus === 'completed' ? 'Task completed!' : 'Task reopened')
      onUpdate()
    } catch (error) {
      toast.error('Failed to update task')
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return

    try {
      await apiClient.delete(`/tasks/${task.id}`)
      toast.success('Task deleted')
      onUpdate()
    } catch (error) {
      toast.error('Failed to delete task')
    }
  }

  return (
    <div className="flex items-start gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
      {/* Checkbox */}
      <button
        onClick={handleToggleComplete}
        className="flex-shrink-0 mt-1 text-gray-400 hover:text-primary-600 transition-colors"
      >
        {task.status === 'completed' ? (
          <CheckCircle className="w-5 h-5" />
        ) : (
          <Circle className="w-5 h-5" />
        )}
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <h4
          className={`font-medium ${
            task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900 dark:text-white'
          }`}
        >
          {task.title}
        </h4>
        {task.description && (
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{task.description}</p>
        )}
        <div className="flex items-center gap-2 mt-2">
          <span
            className={`text-xs px-2 py-1 rounded ${priorityColors[task.priority]}`}
          >
            {task.priority}
          </span>
          {task.estimated_duration && (
            <span className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {task.estimated_duration}m
            </span>
          )}
        </div>
      </div>

      {/* Actions */}
      <button
        onClick={handleDelete}
        className="flex-shrink-0 text-gray-400 hover:text-red-600 transition-colors"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  )
}
