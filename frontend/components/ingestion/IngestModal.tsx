'use client'

import { useState } from 'react'
import { X, FileText, Mic, Image } from 'lucide-react'
import apiClient from '@/lib/api/client'
import toast from 'react-hot-toast'

interface IngestModalProps {
  onClose: () => void
  onSuccess: () => void
}

export function IngestModal({ onClose, onSuccess }: IngestModalProps) {
  const [mode, setMode] = useState<'text' | 'voice' | 'image'>('text')
  const [content, setContent] = useState('')
  const [title, setTitle] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (mode === 'text') {
        const formData = new FormData()
        formData.append('content', content)
        if (title) formData.append('title', title)

        await apiClient.post('/ingestion/text', formData)
        toast.success('Text processed successfully!')
      } else if (mode === 'voice' && file) {
        const formData = new FormData()
        formData.append('file', file)

        await apiClient.post('/ingestion/voice', formData)
        toast.success('Voice recording processed!')
      } else if (mode === 'image' && file) {
        const formData = new FormData()
        formData.append('file', file)

        await apiClient.post('/ingestion/image', formData)
        toast.success('Image processed successfully!')
      }

      onSuccess()
    } catch (error) {
      toast.error('Failed to process input')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Add Task</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Mode Selector */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setMode('text')}
            className={`flex-1 py-2 px-4 rounded-lg flex items-center justify-center gap-2 ${
              mode === 'text'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <FileText className="w-4 h-4" />
            Text
          </button>
          <button
            onClick={() => setMode('voice')}
            className={`flex-1 py-2 px-4 rounded-lg flex items-center justify-center gap-2 ${
              mode === 'voice'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <Mic className="w-4 h-4" />
            Voice
          </button>
          <button
            onClick={() => setMode('image')}
            className={`flex-1 py-2 px-4 rounded-lg flex items-center justify-center gap-2 ${
              mode === 'image'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            <Image className="w-4 h-4" />
            Image
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit}>
          {mode === 'text' && (
            <>
              <input
                type="text"
                placeholder="Title (optional)"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-2 mb-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <textarea
                placeholder="Describe your tasks... AI will extract and organize them for you."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
                rows={8}
                className="w-full px-4 py-2 mb-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              />
            </>
          )}

          {(mode === 'voice' || mode === 'image') && (
            <div className="mb-4">
              <input
                type="file"
                accept={mode === 'voice' ? 'audio/*' : 'image/*'}
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg"
              />
              {file && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  Selected: {file.name}
                </p>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || (mode === 'text' && !content) || ((mode === 'voice' || mode === 'image') && !file)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Processing...' : 'Process'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
