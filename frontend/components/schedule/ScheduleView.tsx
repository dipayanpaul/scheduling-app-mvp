'use client'

import { useEffect, useState } from 'react'
import { format } from 'date-fns'
import apiClient from '@/lib/api/client'
import toast from 'react-hot-toast'
import { RefreshCw } from 'lucide-react'

interface ScheduledTask {
  task_id: string
  task: any
  start_time: string
  end_time: string
  order: number
}

export function ScheduleView() {
  const [schedule, setSchedule] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const today = format(new Date(), 'yyyy-MM-dd')

  useEffect(() => {
    loadSchedule()
  }, [])

  const loadSchedule = async () => {
    setLoading(true)
    try {
      const response = await apiClient.get(`/schedule/${today}`)
      setSchedule(response.data)
    } catch (error) {
      // Schedule doesn't exist yet
      setSchedule(null)
    } finally {
      setLoading(false)
    }
  }

  const generateSchedule = async () => {
    setLoading(true)
    try {
      const response = await apiClient.post('/schedule/generate', {
        date: today,
        force_regenerate: true,
      })
      setSchedule(response.data)
      toast.success('Schedule generated successfully!')
    } catch (error) {
      toast.error('Failed to generate schedule')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (!schedule) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500 mb-4">No schedule for today yet</p>
        <button
          onClick={generateSchedule}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          Generate AI Schedule
        </button>
      </div>
    )
  }

  const tasks: ScheduledTask[] = schedule.tasks || []

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <p className="text-sm text-gray-500">
          {tasks.length} tasks scheduled
        </p>
        <button
          onClick={generateSchedule}
          disabled={loading}
          className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
        >
          <RefreshCw className="w-4 h-4" />
          Regenerate
        </button>
      </div>

      <div className="space-y-3">
        {tasks.map((item) => (
          <div
            key={item.task_id}
            className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg"
          >
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-medium">{item.task?.title || 'Task'}</h4>
              <span className="text-xs text-gray-500">
                {item.start_time} - {item.end_time}
              </span>
            </div>
            {item.task?.description && (
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {item.task.description}
              </p>
            )}
          </div>
        ))}
      </div>

      {schedule.metadata?.ai_generated && (
        <p className="text-xs text-gray-500 mt-4 text-center">
          🤖 AI-generated schedule
        </p>
      )}
    </div>
  )
}
