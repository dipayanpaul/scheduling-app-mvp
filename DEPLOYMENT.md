# Deployment Guide

This guide covers deploying the Scheduling App to production.

## Prerequisites

- Supabase account and project
- Vercel account (for frontend) or similar hosting
- Railway/Render/Fly.io account (for backend) or similar
- Anthropic API key
- Domain name (optional)

## 1. Supabase Setup

### Create Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Create a new project
3. Wait for setup to complete (2-3 minutes)

### Apply Database Migrations

```bash
# Link to your project
supabase link --project-ref your-project-ref

# Push migrations
supabase db push

# Generate TypeScript types (optional)
supabase gen types typescript --local > frontend/types/supabase.ts
```

### Configure Authentication

1. Go to Authentication > Settings
2. Set Site URL to your frontend URL
3. Add Redirect URLs for OAuth callbacks
4. Enable Email provider or social providers as needed

### Get Credentials

From Settings > API:
- Project URL
- `anon` public key
- `service_role` key (keep secret!)

## 2. Backend Deployment

### Environment Variables

Create a `.env` file with:

```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
API_V1_PREFIX=/api/v1
CORS_ORIGINS=https://your-frontend-domain.com

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key-optional
DEFAULT_LLM_PROVIDER=anthropic

# Calendar OAuth (if using)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-api-domain.com/api/v1/calendar/google/callback

LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn-optional
```

### Deploy to Railway (Example)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Add environment variables through Railway dashboard

# Deploy
railway up
```

### Deploy to Render (Example)

1. Connect your GitHub repo
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Deploy to Fly.io (Example)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Set secrets
flyctl secrets set ANTHROPIC_API_KEY=your-key
flyctl secrets set SUPABASE_KEY=your-key
# ... set all required secrets

# Deploy
flyctl deploy
```

## 3. Frontend Deployment

### Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_APP_URL=https://your-frontend-domain.com
```

### Deploy to Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel

# Add environment variables through Vercel dashboard

# Deploy to production
vercel --prod
```

### Deploy to Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Build
cd frontend
npm run build

# Deploy
netlify deploy --prod
```

## 4. Post-Deployment Configuration

### Update CORS Origins

Update backend `CORS_ORIGINS` to include your frontend domain:

```bash
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

### Configure Supabase Edge Functions (Optional)

For background jobs like notification processing:

```bash
# Deploy edge function
supabase functions deploy process-notifications

# Set function secrets
supabase secrets set SUPABASE_KEY=your-service-key
```

### Set up Monitoring

1. **Sentry** (Error Tracking)
   - Create Sentry project
   - Add DSN to environment variables

2. **Uptime Monitoring**
   - Use UptimeRobot, Pingdom, or similar
   - Monitor `/health` endpoint

3. **Log Aggregation**
   - Use Logtail, Papertrail, or CloudWatch

## 5. Security Checklist

- [ ] All secrets are in environment variables (not committed)
- [ ] HTTPS enabled on both frontend and backend
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Database RLS policies active
- [ ] API keys rotated from defaults
- [ ] Backup strategy in place
- [ ] Error reporting configured
- [ ] Authentication tested end-to-end

## 6. Backup Strategy

### Database Backups

Supabase provides automatic daily backups. For additional safety:

```bash
# Manual backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore if needed
psql $DATABASE_URL < backup_20240101.sql
```

### Regular Maintenance

- Monitor database size and performance
- Review audit logs regularly
- Update dependencies monthly
- Test backup restoration quarterly

## 7. Scaling Considerations

### Database
- Enable connection pooling (Supabase has this built-in)
- Add indexes for frequently queried fields
- Consider read replicas for heavy read workloads

### Backend
- Use horizontal scaling (multiple instances)
- Implement Redis for caching
- Use CDN for static assets

### Frontend
- Enable Vercel/Netlify edge functions
- Implement proper caching headers
- Use image optimization

## Troubleshooting

### Common Issues

**CORS Errors**
- Verify `CORS_ORIGINS` includes your frontend domain
- Check for trailing slashes in URLs

**Authentication Failures**
- Verify Supabase URL and keys
- Check JWT expiration settings
- Ensure redirect URLs are configured

**Database Connection Issues**
- Verify connection string
- Check Supabase project status
- Review connection pool limits

**LLM API Errors**
- Verify API keys are correct
- Check rate limits and quotas
- Monitor token usage

## Support

For issues:
1. Check logs in your hosting platform
2. Review Supabase logs
3. Check API endpoint health
4. Review this documentation
5. Open an issue on GitHub
