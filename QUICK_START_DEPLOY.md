# 🚀 QUICK START - Alexandria Deployment

## 📌 TL;DR - Deploy in 5 Steps

### Step 1: Create API Keys (5 min)
```bash
1. Google: https://console.cloud.google.com → Enable "Generative Language API"
2. AssemblyAI: https://www.assemblyai.com → Get API token
3. YouTube: https://console.cloud.google.com → Enable "YouTube Data API v3"
```

### Step 2: Deploy Frontend to Vercel (3 min)
```
1. https://vercel.com/new
2. Import your GitHub repo
3. Click Deploy (uses vercel.json auto-config)
4. Note your Vercel URL
```

### Step 3: Deploy Backend to Render (5 min)
```
1. https://dashboard.render.com/new/web
2. Connect GitHub repo
3. Add env vars (API keys from Step 1)
4. Click Deploy (uses render.yaml auto-config)
5. Note your Render URL
```

### Step 4: Connect Frontend to Backend (2 min)
```
1. Vercel Dashboard → Settings → Environment Variables
2. Edit: VITE_API_BASE_URL = https://your-render-url.onrender.com
3. Click Redeploy
```

### Step 5: Test (2 min)
```
1. Open https://your-app.vercel.app
2. Try "Ingest Video" feature
3. Check browser console (F12) for errors
```

**Total time: ~15 minutes!** 🎉

---

## 📚 Full Documentation

For detailed guides, see:
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **Env Setup**: [ENV_SETUP_GUIDE.md](ENV_SETUP_GUIDE.md)

---

## 🔗 Important URLs

After deployment, you'll have:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | `https://your-app.vercel.app` | User app |
| Backend | `https://your-backend.onrender.com` | API server |
| API Docs | `https://your-backend.onrender.com/docs` | Swagger documentation |

---

## 🎯 Using Each Service

### Vercel (Frontend)
- Auto-deploys on git push
- Handles SPA routing
- ~3-5 minute build time
- Free tier: 100GB/month bandwidth

### Render (Backend)
- Auto-deploys on git push
- Free tier: ~15min spindown
- Keep alive with free pinging
- Upgrade to $7/mo if needed

---

## ✅ Verify Deployment

```bash
# Is frontend live?
curl https://your-app.vercel.app

# Is backend live?
curl https://your-backend.onrender.com/docs

# Can they talk?
Open frontend in browser, open DevTools (F12)
→ Console tab → Network tab → Try a feature
→ Should see successful API call
```

---

## ⚡ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Backend unreachable" | Check `VITE_API_BASE_URL` env var in Vercel |
| CORS errors | Verify backend is running (Render dashboard) |
| 404 on refresh | Check `vercel.json` exists in root |
| API key error | Add all 3 keys to Render environment variables |
| Render down after 15m | Free tier - upgrade or use Uptime Robot |

---

## 🚀 Ready?

→ Start with **DEPLOYMENT_CHECKLIST.md** for step-by-step guide!

Questions? See **DEPLOYMENT.md** for comprehensive documentation.
