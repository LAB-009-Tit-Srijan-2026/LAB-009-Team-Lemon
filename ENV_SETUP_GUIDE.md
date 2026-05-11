# 🔐 Environment Variables Guide - Alexandria

This guide explains all environment variables needed for Alexandria deployment.

## 📋 Overview

### Frontend (Vercel)
- `VITE_API_BASE_URL` - Backend API endpoint

### Backend (Render/Railway/Heroku)
- `GOOGLE_API_KEY` - Google Generative AI API
- `ASSEMBLYAI_API_KEY` - AssemblyAI transcription service
- `YOUTUBE_API_KEY` - YouTube Data API
- `ENABLE_*` flags - Feature toggles

---

## 🚀 Getting API Keys

### 1️⃣ Google API Key (For Gemini AI)

**Purpose**: Summarization and Q&A responses

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "Alexandria"
3. Enable "Generative Language API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the key

**Cost**: Free tier: 60 requests/minute

---

### 2️⃣ AssemblyAI API Key (For Audio Transcription)

**Purpose**: Convert audio/video files to text transcripts

**Steps**:
1. Go to [AssemblyAI](https://www.assemblyai.com)
2. Sign up (free account available)
3. Go to Dashboard
4. Copy "API Token"
5. Add to environment variables

**Cost**: Free tier: 100 minutes/month

---

### 3️⃣ YouTube API Key (Optional)

**Purpose**: Get video metadata, captions, and information

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Same project as Google API
3. Enable "YouTube Data API v3"
4. Go to Credentials → Create API Key
5. Copy the key

**Cost**: Free tier: 10,000 units/day

**Note**: Can skip this if using YouTube captions directly

---

## 🛠️ Local Development Setup

### 1. Create `.env` file in backend directory

```bash
cd backend
cp .env.example .env
```

### 2. Edit `backend/.env`

```env
# API Keys (from steps above)
GOOGLE_API_KEY=your_actual_key_here
ASSEMBLYAI_API_KEY=your_actual_key_here
YOUTUBE_API_KEY=your_actual_key_here

# Feature Flags
ENABLE_GEMINI=1              # Enable AI summaries
ENABLE_CHROMA=1              # Enable ChromaDB persistence
ENABLE_EMBEDDINGS=1          # Enable vector embeddings for Q&A
ENABLE_YOUTUBE_ASR=1         # Try YouTube captions first (free)
ENABLE_METADATA_FALLBACK=0   # Use video metadata if transcript unavailable
```

### 3. Create `frontend/.env.local` for development

```bash
cd ../frontend
cp .env.example .env.local
```

### 4. Edit `frontend/.env.local`

```env
# Local development (backend running on localhost)
VITE_API_BASE_URL=http://localhost:8000

# Or use deployed backend
# VITE_API_BASE_URL=https://your-backend-url.onrender.com
```

---

## 🌐 Production Deployment (Vercel + Render)

### Frontend Environment Variables (Vercel)

Go to: **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**

Add:
```
VITE_API_BASE_URL = https://your-backend-url.onrender.com
```

**Scope**: Production (or all environments)

---

### Backend Environment Variables (Render)

Go to: **Render Dashboard** → Your Service → **Environment**

Add all of:
```
GOOGLE_API_KEY=your_actual_key_from_google
ASSEMBLYAI_API_KEY=your_actual_key_from_assemblyai
YOUTUBE_API_KEY=your_actual_key_from_youtube

ENABLE_GEMINI=1
ENABLE_CHROMA=1
ENABLE_EMBEDDINGS=1
ENABLE_YOUTUBE_ASR=1
ENABLE_METADATA_FALLBACK=0
```

---

## 🔑 Environment Variable Reference

### Backend Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `GOOGLE_API_KEY` | string | - | API key for Generative Language API |
| `ASSEMBLYAI_API_KEY` | string | - | API key for audio transcription |
| `YOUTUBE_API_KEY` | string | - | API key for YouTube metadata |
| `ENABLE_GEMINI` | 0/1 | 0 | Enable AI-powered summaries |
| `ENABLE_CHROMA` | 0/1 | 0 | Enable ChromaDB for persistence |
| `ENABLE_EMBEDDINGS` | 0/1 | 0 | Enable vector embeddings for Q&A |
| `ENABLE_YOUTUBE_ASR` | 0/1 | 1 | Use YouTube captions (no API needed) |
| `ENABLE_METADATA_FALLBACK` | 0/1 | 0 | Use video metadata as fallback |

---

### Frontend Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `VITE_API_BASE_URL` | string | `http://127.0.0.1:8000` | Backend API endpoint URL |

---

## ❓ FAQ

### Q: Do I need all API keys?
**A**: No! Here's the minimum:
- `GOOGLE_API_KEY` - For AI summaries (highly recommended)
- `ENABLE_YOUTUBE_ASR=1` - Use YouTube captions (free, no key needed)

Optional:
- `ASSEMBLYAI_API_KEY` - Only if uploading audio/video files
- `YOUTUBE_API_KEY` - Only if you want advanced YouTube metadata

### Q: What if I don't have API keys yet?
**A**: Start with free tier:
1. Google: 60 requests/min free
2. AssemblyAI: 100 mins/month free
3. YouTube: 10k units/day free

Plenty to test and develop!

### Q: Why does my frontend not connect to backend?
**A**: Check `VITE_API_BASE_URL`:
- Local dev: Should be `http://localhost:8000`
- Production: Should be `https://your-backend-url.onrender.com`
- Frontend rebuilds to use env var - clear cache after setting it

### Q: Can I hide API keys?
**A**: ✅ Yes! Use environment variables:
- Never hardcode in files
- Never commit `.env` files
- Always use `.env.example` templates
- Never paste keys in chat/issues

### Q: Where should I store API keys?
**A**: 
- **Local dev**: In `backend/.env` (gitignored)
- **Production**: In service dashboard (Render settings)
- **Never**: In code or git history

---

## 🚨 Security Best Practices

1. ✅ **Use environment variables** - Never hardcode
2. ✅ **Add .env to .gitignore** - Already done in template
3. ✅ **Rotate keys regularly** - Change keys every 30 days in production
4. ✅ **Use minimal permissions** - Only enable needed APIs
5. ✅ **Monitor usage** - Check API quotas regularly
6. ✅ **Use service keys** - Not personal API keys
7. ✅ **Set rate limits** - Protect against abuse

---

## 🔄 After Setting Variables

### Frontend
```bash
cd frontend
npm run dev
# Should use VITE_API_BASE_URL from .env.local
```

### Backend
```bash
cd backend
uvicorn main:app --reload
# Should load from .env
```

### After Vercel/Render Deployment
```bash
# Frontend redeploys automatically after env var change
# Backend may need manual restart on Render
```

---

## ✅ Verification Checklist

- [ ] All API keys obtained and working
- [ ] `.env` files created from `.env.example`
- [ ] Backend `.env` has all required keys
- [ ] Frontend `.env.local` has correct API_BASE_URL
- [ ] `.env` files in `.gitignore` (not committed)
- [ ] Vercel env vars set correctly
- [ ] Render env vars set correctly
- [ ] Frontend can reach backend (test in browser)
- [ ] API keys are not expired
- [ ] No extra spaces around key values

---

## 📞 Troubleshooting

### "Invalid API Key"
- Copy paste error (extra spaces)
- Key is expired
- Wrong API service
- Free tier quota exceeded

### "Backend unreachable"
- `VITE_API_BASE_URL` is wrong
- Backend not running
- CORS not enabled
- Network/firewall blocking

### "CORS errors"
- Backend CORS middleware not enabled
- Vercel domain not in allowed origins
- Browser privacy/extension blocking

### "Feature not working"
- Required `ENABLE_*` flag is `0`
- Related API key not set
- API quota exceeded
- Service down

---

## 📚 More Information

- [Google Cloud Console](https://console.cloud.google.com)
- [AssemblyAI Dashboard](https://www.assemblyai.com/dashboard)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Render Environment Variables](https://render.com/docs/environment-variables)

---

**Ready to deploy?** Follow the [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
