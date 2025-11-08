# AI-Powered Scheduling App MVP

An intelligent scheduling application with multimodal input, AI-powered task prioritization, and calendar integration.

## Architecture

- **Frontend**: Next.js 14+ with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python) with modular architecture
- **Database**: Supabase (PostgreSQL + Auth)
- **AI**: Anthropic Claude (with provider abstraction for OpenAI/local models)

## Project Structure

```
├── frontend/           # Next.js application
├── backend/            # FastAPI application
├── supabase/          # Supabase configuration and migrations
└── docs/              # Additional documentation
```

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Supabase account
- Anthropic API key (or OpenAI API key)

## Getting Started

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Configure environment variables
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure environment variables
uvicorn main:app --reload
```

### Supabase Setup

```bash
cd supabase
# Install Supabase CLI: https://supabase.com/docs/guides/cli
supabase init
supabase start
supabase db push
```

## Features

- 🤖 AI-powered task scheduling and prioritization
- 📝 Multimodal input (text, voice, images)
- 📅 Calendar integration (Google Calendar, Outlook)
- 🔔 Smart notifications and reminders
- 🎯 Personalized scheduling based on user behavior
- 🔄 Real-time updates
- 🔐 Secure authentication with Supabase Auth

## Development

- Frontend runs on `http://localhost:3000`
- Backend API runs on `http://localhost:8000`
- API documentation available at `http://localhost:8000/docs`

## License

MIT
