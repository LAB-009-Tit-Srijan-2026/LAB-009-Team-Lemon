# 🚀 Complete Step-by-Step Vercel Deployment Guide

## 📋 Prerequisites

Before starting, you need:
- ✅ Your code on GitHub (repository pushed)
- ✅ A Vercel account (free - create at https://vercel.com)
- ✅ Frontend is working locally (`npm run dev` works)
- ✅ `vercel.json` in your project root ✓ (already created)

---

## 🎯 Step-by-Step Deployment

### **STEP 1: Prepare Your Code (5 minutes)**

#### 1.1 Make sure `.env` files are in `.gitignore`

Your `.env` should NEVER be committed to GitHub. Check your `.gitignore`:

```bash
# In your project root, check .gitignore
cat .gitignore | grep -i ".env"
# Should show: .env, .env.local, etc.
```

**What you should see:**
```
.env
.env.local
.env.*.local
```

✅ **Already configured** in your project!

---

#### 1.2 Create `.env.example` in frontend (optional, for documentation)

Already created at: `frontend/.env.example`

Contains:
```env
VITE_API_BASE_URL=http://localhost:8000
```

This is just a template - never commit actual secrets!

---

#### 1.3 Test locally one more time

```bash
# Make sure frontend builds without errors
cd z:\AI-Learning-Companion\frontend
npm run build

# Output should end with: "✓ built in XXXms"
```

✅ **Your frontend builds successfully!**

---

#### 1.4 Commit and push to GitHub

```bash
cd z:\AI-Learning-Companion

# Stage all changes
git add .

# Commit
git commit -m "Add Vercel deployment configuration"

# Push to GitHub
git push origin main
```

**What this does:**
- Uploads all your code to GitHub
- Vercel will pull from here to deploy

---

### **STEP 2: Create/Login to Vercel Account (2 minutes)**

#### Option A: Create New Account
1. Go to **https://vercel.com**
2. Click **"Sign Up"** button (top right)
3. Choose one of:
   - Sign up with **GitHub** (Recommended!)
   - Sign up with **Google**
   - Sign up with **Email**

#### Option B: Login to Existing Account
1. Go to **https://vercel.com**
2. Click **"Login"** button
3. Enter your credentials

**Why GitHub is recommended:**
- Auto-connects your GitHub repos
- Simpler deployment flow
- Auto-redeploy on git push

---

### **STEP 3: Import GitHub Repository (3 minutes)**

#### 3.1 Go to Vercel Dashboard

After logging in, you'll see the Vercel dashboard:
- URL: https://vercel.com/dashboard
- Or click **"Dashboard"** in top menu

#### 3.2 Create New Project

Look for button that says:
- **"Add New"** button (top of page), OR
- **"Create"** button, OR
- **"New Project"** button

Click it → You'll see a menu

#### 3.3 Select "Project"

From the dropdown menu:
```
Add New
  ├─ Project ← Click this
  ├─ Template
  └─ ... (other options)
```

#### 3.4 Import GitHub Repository

You'll see screen: **"Import Git Repository"**

Options:
- **"GitHub"** button ← Click this
- "GitLab"
- "Bitbucket"

After clicking GitHub:
- Vercel will ask for GitHub permission
- Authorize access to your repositories

#### 3.5 Select Your Repository

After authorizing, you'll see a list of your GitHub repos:

Find: **AI-Learning-Companion** (or whatever you named it)

Click on it to select it.

---

### **STEP 4: Configure Build Settings (2 minutes)**

After selecting repo, Vercel will show: **"Configure Project"**

You'll see several fields. **IMPORTANT: These should auto-populate from your `vercel.json`!**

But let's verify/set them manually just in case:

#### 4.1 Project Name
```
Field: Project Name
Value: Alexandria (or any name you like)
Description: This will appear in your URL
Example URL: alexandria-xxxx.vercel.app
```

#### 4.2 Framework
```
Field: Framework (might say "Detected: Vite")
Value: Vite
(if not auto-detected, select from dropdown)
```

#### 4.3 Root Directory
```
Field: Root Directory
Value: .
Description: Root of your repo (not "frontend" folder)
Why: Your vercel.json is in the root
```

#### 4.4 Build Command
```
Field: Build Command
Value: cd frontend && npm install && npm run build

This tells Vercel:
1. Go to frontend folder
2. Install npm packages
3. Run Vite build
```

#### 4.5 Output Directory
```
Field: Output Directory (Post Build Command)
Value: frontend/dist

This tells Vercel where the built files are
(Vite outputs to frontend/dist)
```

#### 4.6 Install Command
```
Field: Install Command
Value: npm install

Standard npm install
```

**Visual Example:**
```
┌─────────────────────────────────────┐
│ Project Configuration               │
├─────────────────────────────────────┤
│ Project Name: Alexandria            │
│ Framework: Vite                     │
│ Root Dir: .                         │
│ Build: cd frontend && npm ins... │
│ Output: frontend/dist               │
│ Install: npm install                │
└─────────────────────────────────────┘
```

---

### **STEP 5: Add Environment Variables (2 minutes)**

#### 5.1 Look for "Environment Variables" Section

On the same configuration page, scroll down to find:
```
Environment Variables
```

#### 5.2 Add Your Backend URL

You have TWO options here:

**Option A: Use localhost (for testing now)**
```
Name:  VITE_API_BASE_URL
Value: http://localhost:8000

This is TEMPORARY - only for testing
Later you'll change it to your Vercel backend URL
```

**Option B: Skip for now**
```
Leave it empty for now
Add it later after backend is deployed
(Frontend will use default from frontend/.env.local)
```

**I recommend Option A for now** (so you can test immediately after deploy)

#### 5.3 Add Variable

Click **"Add New"** or **"+"** button to add:
```
Name:  VITE_API_BASE_URL
Value: http://localhost:8000
Scope: Production (or select all)
```

Then click **"Save"** or **"Add"**

**Visual:**
```
┌─ Environment Variables ─────────────┐
│ Name          │ Value              │
├───────────────┼────────────────────┤
│ VITE_API_... │ http://localhost... │
│ [+ Add New]  │                    │
└────────────────────────────────────┘
```

---

### **STEP 6: Deploy! (30 seconds to wait)**

#### 6.1 Click "Deploy" Button

Find and click the **"Deploy"** button:
- Usually at bottom of page
- Might say "Create Project"
- Might say "Deploy Now"

#### 6.2 Wait for Deployment

Vercel will now:
1. **Download** your code from GitHub
2. **Install** dependencies (`npm install`)
3. **Build** your frontend (`npm run build`)
4. **Upload** to CDN
5. **Deploy** to production

**Status page shows:**
```
Building...
  ├─ Installing dependencies
  ├─ Running build command
  └─ Uploading to Vercel

Deployment in progress...
  ├─ Creating production deployment
  └─ Setting up routing

✓ Deployment complete!
```

**Time:** Usually 2-5 minutes

#### 6.3 View Your Live Site

Once done, Vercel will show:
```
✓ Congratulations!
  Your site is live
  
  Visit: https://alexandria-xxxx.vercel.app
```

**Copy this URL!** This is your frontend URL.

---

### **STEP 7: Verify Your Deployment (1 minute)**

#### 7.1 Visit Your New URL

Open in browser:
```
https://alexandria-xxxx.vercel.app
(Replace xxxx with your actual URL)
```

#### 7.2 Check It Loads

You should see:
- ✅ Alexandria homepage
- ✅ All styling visible
- ✅ Buttons clickable
- ✅ No errors in console

#### 7.3 Check Browser Console (Optional)

Press **F12** or **Right-click → Inspect**

Go to **Console** tab:
- Should be **empty** or show only info logs
- ❌ Should NOT have red errors
- ⚠️ Might have CORS warnings if backend not set up yet (that's OK for now)

---

### **STEP 8: Connect to Backend (Later)**

Once you deploy your **backend** to Render:

#### 8.1 Get Your Backend URL

From Render dashboard:
```
https://alexandria-backend-xxxxx.onrender.com
(Copy this exact URL)
```

#### 8.2 Update Environment Variable in Vercel

1. Go to **Vercel Dashboard**
2. Click on your **"Alexandria"** project
3. Click **"Settings"** tab
4. Click **"Environment Variables"**
5. Find **"VITE_API_BASE_URL"**
6. Click the **"Edit"** icon (pencil)
7. Change from:
   ```
   http://localhost:8000
   ```
   To:
   ```
   https://alexandria-backend-xxxxx.onrender.com
   (Your actual Render URL)
   ```
8. Click **"Save"**

#### 8.3 Redeploy Frontend

After changing env var, you need to redeploy:

1. Go to **Deployments** tab
2. Click on your latest deployment
3. Click **"Redeploy"** button
4. Wait for deployment to complete

New deployment will use the new backend URL!

---

## 📋 Troubleshooting Common Issues

### Issue 1: "Build failed"
**Problem:** Deploy failed during build

**Solutions:**
1. Check build logs in Vercel dashboard
2. Look for error message
3. Common causes:
   - Wrong "Output Directory" setting
   - Typo in build command
   - Missing files

**Fix:**
```
1. Go to Vercel Settings
2. Check Output Directory = frontend/dist
3. Check Build Command = cd frontend && npm install && npm run build
4. Redeploy
```

---

### Issue 2: "404 Page Not Found" on page refresh
**Problem:** Refreshing `/summary` page shows 404

**Solution:**
This is a Single Page App (SPA) routing issue. Vercel needs `vercel.json` with rewrites.

Check:
- ✅ You have `vercel.json` in project root
- ✅ It has the rewrites configuration
- ✅ You redeployed after adding `vercel.json`

If still failing:
1. Delete the deployment
2. Push `vercel.json` to GitHub
3. Redeploy

---

### Issue 3: "Backend unreachable"
**Problem:** Frontend shows "Backend unreachable" error

**Solution:**
1. Backend might not be deployed yet
2. Check `VITE_API_BASE_URL` is correct
3. Verify backend is actually running
4. Try visiting backend URL directly:
   ```
   https://your-backend-url.onrender.com/docs
   Should show Swagger UI
   ```

---

### Issue 4: Slow build times
**Problem:** Build takes 5+ minutes

**Normal causes:**
- First build is slower
- Large node_modules
- Network download time

**Not a problem!** But if persistent:
- Check "Build" logs in Vercel
- Ensure no large files in frontend/

---

### Issue 5: No environment variables being used
**Problem:** Frontend still using localhost:8000

**Solution:**
- Environment variables need a redeploy
- Just setting them isn't enough
- Must redeploy after changing env vars
- Wait for new deployment to complete

---

## ✅ Success Checklist

- [ ] GitHub repo created and code pushed
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Build settings configured correctly
- [ ] Environment variables added
- [ ] Initial deployment successful
- [ ] Frontend URL works and loads
- [ ] No errors in browser console
- [ ] UI renders correctly
- [ ] All pages accessible
- [ ] Backend URL updated (after backend deploy)
- [ ] Redeploy done after env var change

---

## 🎯 Your URLs After Deployment

Once live, you'll have:

| What | URL | Purpose |
|------|-----|---------|
| Frontend | `https://alexandria-xxxx.vercel.app` | Your app users visit this |
| Backend API | `https://backend-xxxx.onrender.com` | Frontend calls this (you set up next) |
| API Docs | `https://backend-xxxx.onrender.com/docs` | For testing API |

---

## 📝 Quick Reference

**Vercel Dashboard URLs:**
- Main Dashboard: https://vercel.com/dashboard
- Project Settings: https://vercel.com/dashboard/[project-name]/settings
- Deployments: https://vercel.com/dashboard/[project-name]/deployments
- Environment Vars: https://vercel.com/dashboard/[project-name]/settings/environment-variables

**Commands if needed:**
```bash
# Local testing before deploy
npm run dev          # Dev server
npm run build        # Test production build
npm run preview      # Preview production build locally

# Git commands
git add .
git commit -m "message"
git push origin main  # Triggers auto-deploy on Vercel
```

---

## 🚀 Next Steps

1. ✅ **Deploy Frontend to Vercel** ← You are here
2. ⏳ **Deploy Backend to Render** (see separate guide)
3. ⏳ **Connect Frontend to Backend** (update env vars)
4. ⏳ **Add API Keys** (Google, AssemblyAI, YouTube)
5. ⏳ **Test Production**

---

## 💡 Pro Tips

1. **Auto-redeploy on git push:**
   - Any push to `main` branch = auto-redeploy
   - No need to manually redeploy each time
   - Perfect for continuous updates!

2. **Preview deployments:**
   - Each git pull request = gets preview URL
   - Test before merging to main
   - Super useful for testing!

3. **Environment variables by environment:**
   - Can have different vars for Preview vs Production
   - Use this for testing vs live API keys

4. **Vercel CLI (optional):**
   - Deploy from command line: `vercel --prod`
   - Download project: `vercel pull`
   - More control and speed

---

## ❓ Common Questions

**Q: Why do I need GitHub?**
A: Vercel integrates with Git for easy deployment and auto-updates. You can also manually upload files, but Git is recommended.

**Q: Can I use GitLab or Bitbucket?**
A: Yes! Vercel supports all three. Same process, just select GitLab/Bitbucket instead of GitHub.

**Q: Do I need to pay?**
A: Nope! Vercel free tier includes:
- Unlimited projects
- Unlimited deployments
- 100GB/month bandwidth
- Perfect for most projects

**Q: What if I want my own domain?**
A: Vercel supports custom domains:
1. Buy domain from GoDaddy, Namecheap, etc.
2. In Vercel Settings → Domains
3. Add your domain
4. Update DNS records (Vercel provides instructions)

**Q: How do I revert to an older deployment?**
A: In Vercel Deployments tab, click any past deployment → "Redeploy"

---

Generated: May 10, 2026  
For: Alexandria AI Learning Companion  
Status: Ready to Deploy! 🚀
