'use client'

import { useEffect, useState } from 'react'
import { TaskList } from '@/components/tasks/TaskList'
import { ScheduleView } from '@/components/schedule/ScheduleView'
import { IngestModal } from '@/components/ingestion/IngestModal'
import { Task } from '@/types'
import apiClient from '@/lib/api/client'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [showIngestModal, setShowIngestModal] = useState(false)

  useEffect(() => {
    loadTasks()
  }, [])

  const loadTasks = async () => {
    try {
      const response = await apiClient.get('/tasks')
      setTasks(response.data)
    } catch (error) {
      toast.error('Failed to load tasks')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Scheduling Dashboard
            </h1>
            <button
              onClick={() => setShowIngestModal(true)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              + Add Task
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Task List */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Tasks</h2>
            {loading ? (
              <div className="text-center py-8">Loading...</div>
            ) : (
              <TaskList tasks={tasks} onTasksChange={loadTasks} />
            )}
          </div>

          {/* Schedule View */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Today's Schedule</h2>
            <ScheduleView />
          </div>
        </div>
      </main>

      {/* Ingest Modal */}
      {showIngestModal && (
        <IngestModal
          onClose={() => setShowIngestModal(false)}
          onSuccess={() => {
            setShowIngestModal(false)
            loadTasks()
          }}
        />
      )}
    </div>
  )
}
