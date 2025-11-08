export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  estimated_duration?: number // in minutes
  scheduled_start?: string // ISO datetime
  scheduled_end?: string // ISO datetime
  actual_start?: string
  actual_end?: string
  tags?: string[]
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Note {
  id: string
  user_id: string
  title?: string
  content: string
  source_type: 'text' | 'voice' | 'image'
  media_url?: string
  transcription?: string
  extracted_tasks?: string[]
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface MediaAsset {
  id: string
  user_id: string
  file_name: string
  file_type: string
  file_size: number
  storage_path: string
  public_url?: string
  metadata?: Record<string, any>
  created_at: string
}

export interface UserPreferences {
  id: string
  user_id: string
  work_hours_start?: string // e.g., "09:00"
  work_hours_end?: string // e.g., "17:00"
  work_days?: number[] // 0-6, where 0 is Sunday
  preferred_break_duration?: number // in minutes
  notification_settings?: {
    email: boolean
    push: boolean
    in_app: boolean
    reminder_minutes_before?: number[]
  }
  calendar_sync_enabled?: boolean
  calendar_providers?: ('google' | 'outlook')[]
  ai_preferences?: {
    auto_schedule: boolean
    priority_weights?: {
      deadline: number
      importance: number
      duration: number
    }
  }
  created_at: string
  updated_at: string
}

export interface Schedule {
  id: string
  user_id: string
  date: string // ISO date
  tasks: ScheduledTask[]
  metadata?: {
    ai_generated: boolean
    adjustments_count: number
    user_satisfaction?: number
  }
  created_at: string
  updated_at: string
}

export interface ScheduledTask {
  task_id: string
  task: Task
  start_time: string
  end_time: string
  order: number
}

export interface ApiResponse<T> {
  data: T
  message?: string
  status: 'success' | 'error'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}
