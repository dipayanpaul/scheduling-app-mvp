'use client'

import { Task } from '@/types'
import { TaskItem } from './TaskItem'

interface TaskListProps {
  tasks: Task[]
  onTasksChange: () => void
}

export function TaskList({ tasks, onTasksChange }: TaskListProps) {
  const pendingTasks = tasks.filter((t) => t.status === 'pending' || t.status === 'in_progress')
  const completedTasks = tasks.filter((t) => t.status === 'completed')

  return (
    <div className="space-y-4">
      {/* Pending Tasks */}
      {pendingTasks.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
            Active ({pendingTasks.length})
          </h3>
          <div className="space-y-2">
            {pendingTasks.map((task) => (
              <TaskItem key={task.id} task={task} onUpdate={onTasksChange} />
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
            Completed ({completedTasks.length})
          </h3>
          <div className="space-y-2 opacity-60">
            {completedTasks.map((task) => (
              <TaskItem key={task.id} task={task} onUpdate={onTasksChange} />
            ))}
          </div>
        </div>
      )}

      {tasks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Add one to get started!
        </div>
      )}
    </div>
  )
}
