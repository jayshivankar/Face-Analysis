# Deployment Guide

Complete guide for deploying Face Health Analyzer to production.

## Overview

This application has two separate deployment targets:
1. **Frontend** (React) - Vercel, Netlify, or similar
2. **Backend** (FastAPI) - Railway, Render, or Heroku

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

**Step 1: Prepare**
```bash
cd frontend
npm run build
```

**Step 2: Deploy**
```bash
npm install -g vercel
vercel
```

**Step 3: Configure Environment**
In Vercel Dashboard → Settings → Environment Variables:
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=https://your-backend-url.railway.app
```

**Step 4: Redeploy**
```bash
vercel --prod
```

---

### Option 2: Netlify

**Step 1: Build**
```bash
cd frontend
npm run build
```

**Step 2: Deploy**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

**Step 3: Configure**
- Go to Site Settings → Environment Variables
- Add the same environment variables as Vercel

---

## Backend Deployment

### Option 1: Railway (Recommended)

**Step 1: Create Railway Project**
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository

**Step 2: Configure**
- **Root Directory:** `backend`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Python Version:** 3.9+

**Step 3: Environment Variables**
In Railway dashboard, add:
```
MODELS_PATH=../saved_models
```

**Step 4: Deploy**
Railway will auto-deploy on push to main branch.

---

### Option 2: Render

**Step 1: Create Web Service**
1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository

**Step 2: Configure**
```
Name: face-health-analyzer-backend
Root Directory: backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Step 3: Environment Variables**
```
MODELS_PATH=../saved_models
```

**Step 4: Deploy**
Click "Create Web Service"

---

### Option 3: Heroku

**Step 1: Create Procfile**
```bash
cd backend
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile
```

**Step 2: Deploy**
```bash
heroku login
heroku create face-health-analyzer
git subtree push --prefix backend heroku main
```

---

## Supabase Setup (Required)

**Step 1: Create Project**
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Wait for database provisioning

**Step 2: Get Credentials**
- Project URL: Settings → API → Project URL
- Anon Key: Settings → API → anon/public key

**Step 3: Database Migration**
The migration will run automatically when your frontend connects for the first time. You can verify in:
- Supabase Dashboard → Table Editor
- Look for `analysis_reports` table

**Step 4: (Optional) Manual Migration**
If needed, you can run the migration manually:
1. Go to SQL Editor in Supabase
2. Copy content from your migration file
3. Run the SQL

---

## Environment Variables Summary

### Frontend (.env)
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VITE_API_URL=https://your-backend.railway.app
```

### Backend (optional)
```env
MODELS_PATH=../saved_models
```

---

## Post-Deployment Checklist

### Frontend
- [ ] Site loads without errors
- [ ] Environment variables are set
- [ ] Theme toggle works
- [ ] Image upload works
- [ ] Webcam access works (requires HTTPS)
- [ ] API calls succeed

### Backend
- [ ] `/health` endpoint returns 200
- [ ] `/docs` shows Swagger UI
- [ ] Models load successfully
- [ ] CORS configured correctly
- [ ] File uploads work

### Database
- [ ] Supabase connection works
- [ ] Reports save successfully
- [ ] RLS policies allow access
- [ ] Data persists after refresh

---

## Common Issues

### Issue: CORS Errors
**Solution:** Update `main.py` CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Models Not Loading
**Solution:**
1. Ensure `saved_models/` is in the correct relative path
2. Check file sizes (should not be Git LFS pointers)
3. Verify Python can access the files

### Issue: Webcam Not Working
**Solution:**
- Webcam requires HTTPS in production
- Check browser permissions
- Vercel/Netlify automatically provide HTTPS

### Issue: Large Build Size
**Solution:**
1. Implement code splitting in `vite.config.js`
2. Use dynamic imports for heavy components
3. Optimize images and assets

### Issue: Slow API Response
**Solution:**
1. Use Railway/Render paid plan for better resources
2. Implement caching for model predictions
3. Add CDN for static assets

---

## Performance Optimization

### Frontend
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'chart-vendor': ['recharts'],
          'motion-vendor': ['framer-motion'],
        },
      },
    },
  },
}
```

### Backend
- Use gunicorn with multiple workers:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Monitoring

### Frontend
- **Vercel:** Built-in analytics
- **Netlify:** Built-in analytics
- Add Sentry for error tracking

### Backend
- **Railway:** Built-in metrics
- **Render:** Built-in metrics
- Add logging with Python logging module

### Database
- **Supabase:** Dashboard shows usage
- Monitor query performance
- Check RLS policy execution

---

## Backup Strategy

### Database
1. Supabase has automatic backups
2. Manual export: Dashboard → Database → Backups
3. Download as SQL or CSV

### Models
1. Keep original model files in version control (Git LFS)
2. Backup to cloud storage (S3, Google Cloud Storage)

---

## Scaling

### Horizontal Scaling
- **Frontend:** CDN automatically scales
- **Backend:** Add more Railway/Render instances
- **Database:** Supabase scales automatically

### Vertical Scaling
- Upgrade Railway/Render plan for more resources
- Optimize model inference (quantization, pruning)

---

## CI/CD Setup

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        # Railway CLI commands here
```

---

## Security Checklist

- [ ] Environment variables stored securely
- [ ] HTTPS enabled (automatic on Vercel/Netlify)
- [ ] CORS properly configured
- [ ] Rate limiting added (optional)
- [ ] Input validation on backend
- [ ] Supabase RLS policies tested
- [ ] No secrets in code/Git
- [ ] Regular dependency updates

---

## Cost Estimate

### Free Tier (Perfect for Personal/Demo)
- **Vercel/Netlify:** Free for personal projects
- **Railway:** $5/month credit (enough for small projects)
- **Supabase:** Free tier includes 500MB database
- **Total:** $0-5/month

### Production Tier
- **Vercel Pro:** $20/month
- **Railway Pro:** ~$10-20/month
- **Supabase Pro:** $25/month
- **Total:** ~$55-65/month

---

## Support

- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Supabase Docs:** [supabase.com/docs](https://supabase.com/docs)

---

**Your application is now deployed and accessible worldwide!** 🌍
