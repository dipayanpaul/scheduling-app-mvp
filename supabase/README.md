# Supabase Configuration

This directory contains the Supabase configuration and database migrations for the Scheduling App.

## Setup

1. **Install Supabase CLI**
   ```bash
   npm install -g supabase
   # or
   brew install supabase/tap/supabase
   ```

2. **Initialize Supabase (if not already done)**
   ```bash
   supabase init
   ```

3. **Start Local Supabase**
   ```bash
   supabase start
   ```

4. **Apply Migrations**
   ```bash
   supabase db push
   ```

5. **Access Supabase Studio**
   - Open `http://localhost:54323` in your browser
   - This provides a GUI for managing your database

## Database Schema

The database includes the following main tables:

- **tasks**: User tasks with priority, status, and scheduling information
- **notes**: Notes from various sources (text, voice, image)
- **media_assets**: Uploaded files and media
- **user_preferences**: User settings and preferences
- **schedules**: AI-generated daily schedules
- **scheduling_history**: Historical data for learning and analytics
- **notifications**: Notification queue
- **audit_logs**: Activity audit trail
- **calendar_integrations**: External calendar sync configuration

## Row Level Security (RLS)

All tables have RLS enabled with policies ensuring users can only access their own data.

## Connecting to Production

1. **Link to Production Project**
   ```bash
   supabase link --project-ref your-project-ref
   ```

2. **Push Migrations to Production**
   ```bash
   supabase db push
   ```

3. **Update Environment Variables**
   - Get your Supabase URL and keys from the Supabase dashboard
   - Update `.env` files in both frontend and backend

## Useful Commands

- `supabase status` - Check status of local services
- `supabase db reset` - Reset database and reapply migrations
- `supabase gen types typescript` - Generate TypeScript types from schema
- `supabase stop` - Stop local Supabase services

## Migrations

Migrations are stored in `migrations/` directory and are applied in order by timestamp.

To create a new migration:
```bash
supabase migration new your_migration_name
```
