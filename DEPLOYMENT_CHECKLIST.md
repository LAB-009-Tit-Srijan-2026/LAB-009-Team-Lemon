# 📋 Deployment Checklist - Alexandria

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] Project pushed to GitHub
- [ ] `.env` files are in `.gitignore` (do NOT commit API keys)
- [ ] `vercel.json` is in repository root
- [ ] `.vercelignore` is in repository root
- [ ] `render.yaml` is in repository root

### ✅ Frontend Configuration
- [ ] `frontend/package.json` has build script: `"build": "vite build"`
- [ ] `vite.config.js` exists and is correct
- [ ] `frontend/src/api/client.js` uses `VITE_API_BASE_URL` environment variable
- [ ] No hardcoded API URLs in frontend code
- [ ] `.env.example` has `VITE_API_BASE_URL` template

### ✅ Backend Configuration
- [ ] `backend/requirements.txt` includes all dependencies
- [ ] `backend/main.py` has CORS middleware enabled
- [ ] CORS allows requests from your Vercel domain
- [ ] Environment variables are read from `.env`
- [ ] Backend uses proper port from `$PORT` environment variable

---

## Frontend Deployment to Vercel

### 1️⃣ Initial Setup (One Time)

- [ ] Create Vercel account at [vercel.com](https://vercel.com)
- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Authenticate: `vercel login`

### 2️⃣ Connect Repository

- [ ] Go to [vercel.com/new](https://vercel.com/new)
- [ ] Click "Import Project"
- [ ] Select your GitHub repository
- [ ] Choose "Alexandria" project name (or custom)

### 3️⃣ Configure Build Settings

- [ ] **Framework**: Vite
- [ ] **Root Directory**: `.` (root of repo)
- [ ] **Build Command**: `cd frontend && npm install && npm run build`
- [ ] **Output Directory**: `frontend/dist`
- [ ] **Install Command**: `npm install`

### 4️⃣ Set Environment Variables

- [ ] Click "Environment Variables"
- [ ] Add: `VITE_API_BASE_URL` = `http://localhost:8000` (temporarily for testing)
- [ ] Don't deploy yet! First deploy backend.

### 5️⃣ Deploy

- [ ] Click "Deploy"
- [ ] Wait for deployment (~2-3 minutes)
- [ ] Note your Vercel URL: `https://your-app.vercel.app`

---

## Backend Deployment to Render

### 1️⃣ Setup Render Account

- [ ] Create account at [render.com](https://render.com)
- [ ] Create free tier account (optional paid later)

### 2️⃣ Deploy via GitHub

- [ ] Go to [dashboard.render.com](https://dashboard.render.com)
- [ ] Click "New +" → "Web Service"
- [ ] Select "Build and deploy from a Git repository"
- [ ] Connect GitHub
- [ ] Select your Alexandria repository

### 3️⃣ Configure Service

- [ ] **Name**: `alexandria-backend`
- [ ] **Region**: Select closest to your users (Oregon, Virginia, etc.)
- [ ] **Branch**: `main`
- [ ] **Runtime**: `Python 3.11`
- [ ] **Build Command**: `pip install -r backend/requirements.txt`
- [ ] **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] **Plan**: Free (or Pro if you want more resources)

### 4️⃣ Add Environment Variables

Click "Advanced" → "Environment Variables", then add:

```
GOOGLE_API_KEY=your_actual_key
ASSEMBLYAI_API_KEY=your_actual_key
YOUTUBE_API_KEY=your_actual_key
ENABLE_GEMINI=1
ENABLE_CHROMA=1
ENABLE_EMBEDDINGS=1
ENABLE_YOUTUBE_ASR=1
ENABLE_METADATA_FALLBACK=0
```

### 5️⃣ Deploy

- [ ] Click "Create Web Service"
- [ ] Wait for deployment (~5-10 minutes)
- [ ] Note your backend URL from dashboard (e.g., `https://alexandria-backend-xxxx.onrender.com`)

### 6️⃣ Keep Backend Awake (Free Tier)

- [ ] Render free tier spins down after 15 mins of inactivity
- [ ] To keep it always running:
  - [ ] Upgrade to paid tier ($7/month), OR
  - [ ] Use a pinging service (Uptime Robot) to keep it alive

---

## Link Frontend to Backend

### Step 1: Get Backend URL
- [ ] From Render dashboard, copy your backend service URL
- [ ] Format: `https://alexandria-backend-xxxxx.onrender.com`

### Step 2: Update Vercel Environment Variables
- [ ] Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- [ ] Select your Alexandria project
- [ ] Settings → Environment Variables
- [ ] Edit `VITE_API_BASE_URL`
- [ ] Change from `http://localhost:8000` to your Render URL
- [ ] Save

### Step 3: Redeploy Frontend
- [ ] Vercel Dashboard → Deployments
- [ ] Click on latest deployment
- [ ] Click "Redeploy"
- [ ] Wait for new deployment

---

## Testing & Verification

### ✅ Frontend is Live
- [ ] Visit `https://your-app.vercel.app`
- [ ] Page loads without errors
- [ ] No "500 Server Error"

### ✅ Backend is Responding
- [ ] Visit `https://your-backend-url.com/docs`
- [ ] See FastAPI Swagger documentation
- [ ] Try a test endpoint (e.g., POST to `/ingest`)

### ✅ Frontend ↔ Backend Communication
- [ ] In browser, open Developer Tools (F12)
- [ ] Go to Console tab
- [ ] Try "Ingest Video" feature
- [ ] No CORS errors in console
- [ ] Request shows in Network tab
- [ ] Backend returns correct response

### ✅ Core Features Work
- [ ] [ ] Can paste YouTube URL
- [ ] [ ] Video ingestion starts
- [ ] [ ] Can wait for processing
- [ ] [ ] Summary appears after processing
- [ ] [ ] Can ask questions in chat
- [ ] [ ] Timeline navigation works
- [ ] [ ] Responsive on mobile

---

## Troubleshooting

### CORS Errors
**Problem**: Browser shows CORS errors
**Solution**:
1. Verify backend URL is correct in frontend env vars
2. Check `backend/main.py` has CORS middleware:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
   ```
3. Restart backend service
4. Clear browser cache and reload

### Backend Not Responding (Render Free Tier)
**Problem**: After 15 mins, backend returns 503
**Solution**:
1. Use Uptime Robot to ping every 10 mins
2. Upgrade to paid tier ($7/month)
3. Deploy to Railway/Heroku instead (have better free tiers)

### 404 on Frontend Routes
**Problem**: Refreshing `/summary` page shows 404
**Solution**:
1. `vercel.json` should have rewrites - verify it exists
2. Rebuild on Vercel
3. Clear cache

### Large File Uploads Fail
**Problem**: "Timeout" on file upload
**Solution**:
1. Render free tier has 30s timeout for requests
2. Upgrade to paid or use different service
3. Split large files into chunks

### API Keys Not Working
**Problem**: "Invalid API key" errors
**Solution**:
1. Verify keys are correct on service dashboard
2. Don't have leading/trailing spaces in keys
3. Check keys are for correct service (Google, not Azure)

---

## Production Optimization

### Performance
- [ ] Enable CDN caching in Vercel
- [ ] Compress assets (Vite does this automatically)
- [ ] Use lazy loading for components
- [ ] Monitor Vercel Analytics

### Security
- [ ] Never commit `.env` files
- [ ] Use environment variables for all secrets
- [ ] Enable CORS restrictions (not just `*`)
- [ ] Use HTTPS everywhere (automatic on Vercel)
- [ ] Consider rate limiting for API

### Monitoring
- [ ] Set up Vercel error tracking
- [ ] Monitor backend logs on Render
- [ ] Set up alerts for errors
- [ ] Check usage and billing regularly

### Scaling
- [ ] If users increase:
  - [ ] Consider paid tiers
  - [ ] Enable database persistence (ChromaDB)
  - [ ] Use caching strategies
  - [ ] Consider serverless alternatives

---

## URLs & Useful Links

### After Deployment
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend-url.onrender.com`
- **API Docs**: `https://your-backend-url.onrender.com/docs`
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Render Dashboard**: https://dashboard.render.com

### Support
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Vite Docs: https://vitejs.dev

---

## 🎉 Success!

If all checkboxes are completed and tests pass, your Alexandria instance is **live and ready**!

Share the frontend URL with users:
```
https://your-app.vercel.app
```

**Need help?** Check the full `DEPLOYMENT.md` guide or create an issue on GitHub.
