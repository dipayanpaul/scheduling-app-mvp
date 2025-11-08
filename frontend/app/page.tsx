import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-5xl w-full">
        <h1 className="text-5xl font-bold mb-8 text-center">
          AI-Powered Scheduling App
        </h1>
        <p className="text-xl text-center mb-12 text-gray-600 dark:text-gray-400">
          Intelligent task management with multimodal input and AI-powered prioritization
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <div className="p-6 border rounded-lg hover:border-primary-500 transition-colors">
            <h2 className="text-2xl font-semibold mb-3">🤖 AI Scheduling</h2>
            <p className="text-gray-600 dark:text-gray-400">
              Smart task prioritization and scheduling powered by Claude AI
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:border-primary-500 transition-colors">
            <h2 className="text-2xl font-semibold mb-3">📝 Multimodal Input</h2>
            <p className="text-gray-600 dark:text-gray-400">
              Add tasks via text, voice recordings, or images
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:border-primary-500 transition-colors">
            <h2 className="text-2xl font-semibold mb-3">📅 Calendar Sync</h2>
            <p className="text-gray-600 dark:text-gray-400">
              Seamless integration with Google Calendar and Outlook
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:border-primary-500 transition-colors">
            <h2 className="text-2xl font-semibold mb-3">🔔 Smart Reminders</h2>
            <p className="text-gray-600 dark:text-gray-400">
              Intelligent notifications based on your schedule and priorities
            </p>
          </div>
        </div>

        <div className="flex justify-center gap-4">
          <Link
            href="/auth/login"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
          >
            Get Started
          </Link>
          <Link
            href="/dashboard"
            className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-lg hover:border-primary-600 transition-colors font-semibold"
          >
            View Dashboard
          </Link>
        </div>
      </div>
    </main>
  )
}
