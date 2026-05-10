# 🚀 Deployment Guide - Alexandria

This guide helps you deploy Alexandria to Vercel (frontend) and choose a backend service.

## 📋 Project Overview

- **Frontend**: React 19 + Vite (Deploys to Vercel)
- **Backend**: Python FastAPI (Deploy separately - Render, Railway, or your own server)
- **Extension**: Chrome Extension (Deploy separately via Chrome Web Store)

---

## 🎯 Quick Start Deployment

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- GitHub account with your repository pushed
- API keys ready (Google, AssemblyAI, YouTube)

---

## 🌐 Option 1: Deploy Frontend to Vercel (Recommended)

### Step 1: Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Select your repository

### Step 2: Configure Build Settings

Vercel should automatically detect your Vite setup. Verify:

- **Framework**: Vite
- **Root Directory**: `./` (root of repo)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `npm install`

### Step 3: Add Environment Variables

In the Vercel dashboard, go to **Settings** → **Environment Variables**

Add:
```
VITE_API_BASE_URL = https://your-backend-api.com
```

Where `your-backend-api.com` is where you deploy your backend.

### Step 4: Deploy

Click **Deploy**. Your frontend will be live in ~2 minutes!

---

## 🐍 Backend Deployment Options

Since the backend is Python FastAPI, choose one:

### Option A: Deploy to Render (Easiest for Python)

1. Go to [render.com](https://render.com)
2. Click "Create New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `alexandria-backend`
   - **Region**: Choose closest to users
   - **Branch**: `main`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

5. Add Environment Variables:
   ```
   GOOGLE_API_KEY=your_key_here
   ASSEMBLYAI_API_KEY=your_key_here
   YOUTUBE_API_KEY=your_key_here
   ENABLE_GEMINI=1
   ENABLE_CHROMA=1
   ENABLE_EMBEDDINGS=1
   ```

6. Create the service - it will give you a URL like `https://alexandria-backend.onrender.com`

### Option B: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add `backend/requirements.txt` - Railway auto-detects Python
5. Configure environment variables same as above
6. Get your URL and update Vercel env vars

### Option C: Deploy to Heroku

1. Go to [heroku.com](https://heroku.com)
2. Create new app
3. Connect GitHub repository
4. Set buildpacks:
   - `heroku/python`
5. Add environment variables
6. Deploy

---

## 🔗 Link Frontend to Backend

After deploying backend, update Vercel environment variable:

1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update `VITE_API_BASE_URL` to your backend URL (e.g., `https://alexandria-backend.onrender.com`)
3. **Redeploy** the frontend for changes to take effect

---

## 🔐 Environment Variables Setup

### Frontend (.vercel environment variables)
```
VITE_API_BASE_URL=https://your-backend-url.com
```

### Backend (Render/Railway/Heroku environment variables)
```
GOOGLE_API_KEY=your_google_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
ENABLE_GEMINI=1
ENABLE_CHROMA=1
ENABLE_EMBEDDINGS=1
```

---

## 📝 Local Development

### Frontend
```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

### Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run server
uvicorn backend.main:app --reload
# API at http://localhost:8000
```

---

## 🧪 Test the Connection

After deployment, test the API connection:

```bash
# Frontend test
curl -s https://your-vercel-app.vercel.app/ | grep -i "alexandria"

# Backend test
curl -s https://your-backend-url.com/docs
# Should show FastAPI Swagger docs
```

---

## 🛠️ Troubleshooting

### CORS Issues
If you see CORS errors in browser console:
1. Backend `main.py` already has CORS middleware
2. Verify backend URL in frontend env vars
3. Check backend is running and accessible

### 404 on Frontend Routes
Vercel's `vercel.json` includes rewrites to handle SPA routing. If issues persist:
1. Verify `vercel.json` is in root directory
2. Redeploy on Vercel
3. Clear browser cache

### Backend Connection Fails
1. Test backend URL directly: `curl https://your-backend-url.com/docs`
2. Verify `VITE_API_BASE_URL` is set in Vercel
3. Check CORS headers in backend response
4. Ensure no firewall blocking requests

### Large File Upload Issues
For AssemblyAI uploads, configure backend:
- Increase timeout in Render/Railway settings
- Use streaming uploads
- Consider file size limits

---

## 🚀 Production Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Render/Railway/Heroku
- [ ] Environment variables set on both
- [ ] Frontend → Backend connection tested
- [ ] CORS configured properly
- [ ] SSL/HTTPS working
- [ ] Database persisted (ChromaDB configured)
- [ ] API keys secured (not in code)
- [ ] Logging enabled for debugging
- [ ] Custom domain configured (optional)

---

## 📞 Support

For issues:
1. Check Vercel logs: Dashboard → Deployment → Logs
2. Check backend logs: Platform dashboard (Render/Railway/Heroku)
3. Check browser console for errors
4. Review `backend/main.py` CORS configuration

---

## 🎉 You're Live!

Your Alexandria instance is now deployed! Share the URL with users.

**Frontend URL**: `https://your-app.vercel.app`  
**API Docs**: `https://your-backend-url.com/docs`
