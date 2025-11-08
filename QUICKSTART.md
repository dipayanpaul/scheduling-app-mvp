# Quick Start Guide

Get the AI-Powered Scheduling App running locally in minutes.

## Prerequisites Check

```bash
# Check Node.js (need 18+)
node --version

# Check Python (need 3.11+)
python3 --version

# Install Supabase CLI
npm install -g supabase
```

## 5-Minute Setup

### 1. Start Supabase (1 min)

```bash
cd supabase
supabase start
```

This will output your local Supabase credentials. Copy them!

### 2. Configure Environment (2 min)

**Backend** (.env):
```bash
cd backend
cp .env.example .env

# Edit .env and add:
# - SUPABASE_URL and keys from step 1
# - ANTHROPIC_API_KEY (get from https://console.anthropic.com)
# - SECRET_KEY (generate with: openssl rand -hex 32)
```

**Frontend** (.env.local):
```bash
cd frontend
cp .env.example .env.local

# Edit .env.local and add:
# - NEXT_PUBLIC_SUPABASE_URL from step 1
# - NEXT_PUBLIC_SUPABASE_ANON_KEY from step 1
```

### 3. Start Backend (1 min)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/api/v1/docs

### 4. Start Frontend (1 min)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

## First Steps

1. **Visit** http://localhost:3000
2. **Sign up** for an account
3. **Add a task** using the "+ Add Task" button
4. **Generate schedule** with AI
5. **Explore** the dashboard!

## Troubleshooting

**"Port already in use"**
```bash
# Kill process on port 3000 or 8000
lsof -ti:3000 | xargs kill
lsof -ti:8000 | xargs kill
```

**"Supabase connection failed"**
```bash
supabase stop
supabase start
# Copy new credentials to .env files
```

**"Module not found" errors**
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && rm -rf node_modules && npm install
```

## Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development guide
- Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details
- Read [DEPLOYMENT.md](DEPLOYMENT.md) when ready to deploy

## Getting Help

- Check Supabase Studio: http://localhost:54323
- Check API docs: http://localhost:8000/api/v1/docs
- Review logs in terminal windows
- Check browser console for frontend issues
