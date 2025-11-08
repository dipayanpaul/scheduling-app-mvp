# Development Guide

This guide covers local development setup and best practices.

## Initial Setup

### 1. Install Prerequisites

**Node.js & npm**
```bash
# Install Node.js 18+ from https://nodejs.org
node --version  # Should be 18+
npm --version
```

**Python**
```bash
# Install Python 3.11+
python --version  # Should be 3.11+
```

**Supabase CLI**
```bash
# macOS
brew install supabase/tap/supabase

# Windows/Linux
npm install -g supabase
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd scheduling-app-mvp

# Copy environment files
cp frontend/.env.example frontend/.env.local
cp backend/.env.example backend/.env
```

### 3. Start Supabase Locally

```bash
cd supabase
supabase start

# Note the API URL and anon key from output
# Update frontend/.env.local and backend/.env with these values
```

### 4. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .env
# ANTHROPIC_API_KEY=sk-...

# Run the server
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/api/v1/docs`

### 5. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Project Structure

```
scheduling-app-mvp/
├── frontend/                 # Next.js application
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and clients
│   ├── types/               # TypeScript types
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── tests/              # Test files
│   ├── main.py             # Application entry
│   └── requirements.txt
│
├── supabase/               # Database and config
│   ├── migrations/         # SQL migrations
│   └── config.toml
│
└── README.md
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend type checking
   cd frontend
   npm run type-check
   npm run lint
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

### Database Migrations

**Create a new migration:**
```bash
cd supabase
supabase migration new your_migration_name
```

Edit the generated SQL file in `supabase/migrations/`

**Apply migrations:**
```bash
supabase db reset  # Resets and applies all migrations
```

**Generate TypeScript types from schema:**
```bash
supabase gen types typescript --local > ../frontend/types/supabase.ts
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_tasks.py

# Run specific test
pytest tests/test_tasks.py::test_create_task_success
```

### Frontend Tests

```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint

# Build check
npm run build
```

### Manual Testing

1. **Create a test user**
   - Go to `http://localhost:3000`
   - Sign up with a test email
   - Verify in Supabase Studio (`http://localhost:54323`)

2. **Test API endpoints**
   - Visit `http://localhost:8000/api/v1/docs`
   - Use the interactive API documentation
   - Test authentication flows

3. **Test features**
   - Create tasks
   - Generate AI schedules
   - Test multimodal ingestion
   - Verify notifications

## Common Tasks

### Reset Database

```bash
cd supabase
supabase db reset
```

### View Logs

**Backend:**
```bash
# Logs are printed to console
# Structured JSON logs in production
```

**Frontend:**
```bash
# Check browser console
# Next.js logs in terminal
```

**Supabase:**
```bash
# Open Supabase Studio
open http://localhost:54323
# Check Logs section
```

### Add a New API Endpoint

1. Create route in `backend/app/api/v1/endpoints/your_endpoint.py`
2. Add to router in `backend/app/api/v1/router.py`
3. Add corresponding frontend API call
4. Add tests
5. Update documentation

### Add a New Database Table

1. Create migration: `supabase migration new add_table_name`
2. Write SQL in migration file
3. Add RLS policies
4. Apply migration: `supabase db reset`
5. Update TypeScript types
6. Create corresponding backend models

## Code Style

### Backend (Python)

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small
- Use async/await for I/O operations

Example:
```python
async def get_task(task_id: str, user_id: str) -> Task:
    """
    Retrieve a task by ID for a specific user

    Args:
        task_id: UUID of the task
        user_id: UUID of the user

    Returns:
        Task object if found

    Raises:
        HTTPException: If task not found
    """
    # Implementation
```

### Frontend (TypeScript)

- Use TypeScript strictly
- Prefer functional components
- Use hooks for state management
- Keep components small and focused
- Extract reusable logic to hooks

Example:
```typescript
interface TaskItemProps {
  task: Task
  onUpdate: () => void
}

export function TaskItem({ task, onUpdate }: TaskItemProps) {
  // Implementation
}
```

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill

# Kill process on port 8000
lsof -ti:8000 | xargs kill
```

### Supabase Connection Issues

```bash
# Check Supabase status
supabase status

# Restart Supabase
supabase stop
supabase start
```

### Python Dependencies Issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Node Modules Issues

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Supabase Documentation](https://supabase.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com)
- [Tailwind CSS](https://tailwindcss.com/docs)

## Getting Help

- Check existing documentation
- Review error messages carefully
- Search GitHub issues
- Ask in team chat or forums
