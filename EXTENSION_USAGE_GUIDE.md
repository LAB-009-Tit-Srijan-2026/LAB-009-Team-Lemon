# 🔌 Alexandria v2.0 Chrome Extension - Complete Usage Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [Initial Setup](#initial-setup)
3. [Features Overview](#features-overview)
4. [Step-by-Step Usage](#step-by-step-usage)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Step 1: Ensure Backend is Running
```bash
cd z:\AI-Learning-Companion
uvicorn backend.main:app --port 8001
```
✅ Backend should be running on `http://127.0.0.1:8001`

### Step 2: Load Extension in Chrome

1. **Open Chrome** and go to: `chrome://extensions/`
2. **Enable Developer Mode** (toggle in top-right corner)
3. Click **"Load unpacked"**
4. Navigate to: `z:\AI-Learning-Companion\extension\`
5. Select the `extension` folder
6. ✅ Extension should appear in your Chrome toolbar

### Step 3: Verify Installation
- You should see the **Alexandria icon** (🌿) in your Chrome toolbar
- Click it to verify the popup opens correctly

---

## ⚙️ Initial Setup

### First Time: Configure API URL
1. Click the **Alexandria extension icon** in your toolbar
2. Click the **⚙️ Settings button** (bottom-left of popup)
3. Ensure it shows: `http://127.0.0.1:8001`
4. Click OK to save

### Create Your Account
1. In the extension popup, choose: **Sign Up** tab
2. Enter:
   - **Username**: Something unique (e.g., `john_learner`)
   - **Email**: Your email address
   - **Password**: At least 8 characters (e.g., `MySecurePass123`)
   - **Full Name** (Optional): Your name
3. Click **"Create Account"**
4. ✅ Success! You'll automatically log in

### Or Login if You Have an Account
1. Go to **Login** tab
2. Enter your email and password
3. Click **"Login"**
4. ✅ Ready to use!

---

## 🎯 Features Overview

| Feature | What It Does | Best For |
|---------|-------------|----------|
| 📝 **Summary** | AI-powered video summaries | Quickly understand videos |
| 💬 **Q&A** | Ask questions about video content | Get specific answers |
| 📤 **Export** | Save to Notion, Word, Markdown, Google Docs | Share & organize notes |
| 🌍 **Languages** | Translate summaries to 12 languages | Learn in your language |
| 🎵 **Streaming** | Add Spotify episodes & podcasts | Summarize audio content |
| 📚 **Library** | View all saved videos | Access your collection |

---

## 📖 Step-by-Step Usage

### 🔥 Quick Start: YouTube Video Summary

1. **Open any YouTube video** in your browser
2. **Click the Alexandria icon** in your toolbar (extension popup opens)
3. Go to **📝 Summary** tab
4. Click **"⚡ Generate Summary"** button
5. ⏳ Wait for processing (may take 10-30 seconds)
6. ✅ Summary appears below the button

**Result:**
- Shows Job ID and Status
- Displays a preview summary
- Full summary available on the web app at `http://localhost:5174`

---

### 💬 Ask Questions About a Video

1. **Have a video summary** (Generate one first if you haven't)
2. Go to **💬 Q&A** tab
3. Type your question in the text area:
   - "What is the main topic?"
   - "Who are the key speakers?"
   - "What are the key takeaways?"
4. Click **"Ask Question"** button
5. ✅ Answer appears in the output area

---

### 📤 Export Summary to Different Formats

1. **Generate a summary** first (📝 Summary tab)
2. Go to **📤 Export** tab
3. Select export format:
   - 📄 **Markdown** - Plain text with formatting
   - 📘 **Word (.docx)** - Editable document
   - 📌 **Notion** - Push directly to Notion
   - 🔗 **Google Docs** - Create in Google Drive
4. Click **"Export Summary"** button
5. ✅ Success! Link appears - click to open

**Pro Tip:** All formats support full formatting and timestamps!

---

### 💾 Save Video to Your Library

1. **While watching a YouTube video**, go to **📤 Export** tab
2. Click **"💾 Save to Library"** button
3. ✅ Video is now saved to your personal library

View later:
- Go to **📚 Library** tab
- Click **"🔄 Refresh Library"**
- See all your saved videos with dates

---

### 🌍 Translate Summaries to Other Languages

1. **Generate a summary** first
2. Go to **🌍 Languages** tab
3. Select a language from dropdown:
   - 🇪🇸 Spanish
   - 🇫🇷 French
   - 🇩🇪 German
   - 🇮🇹 Italian
   - 🇵🇹 Portuguese
   - 🇯🇵 Japanese
   - 🇨🇳 Chinese
   - 🇰🇷 Korean
   - 🇷🇺 Russian
   - 🇸🇦 Arabic
   - 🇮🇳 Hindi
4. Click **"🔄 Translate"** button
5. ✅ Translation appears below

---

### 🎵 Add Spotify Episodes & Podcasts

1. Go to **🎵 Streaming** tab
2. **Find your content:**
   - **Spotify**: Copy episode link (e.g., `https://open.spotify.com/episode/ABC123`)
   - **Podcasts**: Copy RSS feed URL or episode link
3. Paste URL in the text field
4. Click **"➕ Add Content"** button
5. ✅ Content is added! Process starts in background

**Examples of supported URLs:**
```
https://open.spotify.com/episode/3OFQGUR0WtKYD5xNfkwPRy
https://podcasts.google.com/feed/abc123
https://feeds.example.com/podcast-rss.xml
```

---

## 🔧 Troubleshooting

### ❌ "Not on a YouTube video" Error
**Problem:** You're not on YouTube
**Solution:** Open a YouTube video first, then click the extension

### ❌ "Login failed" or "Email not found"
**Problem:** Wrong email or password
**Solution:** 
1. Check spelling carefully
2. Reset password (if available) or create new account
3. Ensure password is at least 8 characters

### ❌ "Failed to connect to API"
**Problem:** Backend is not running
**Solution:**
```bash
# In terminal, run:
uvicorn backend.main:app --port 8001

# You should see:
# INFO: Uvicorn running on http://127.0.0.1:8001
```

### ❌ "API Base URL is wrong"
**Problem:** Extension is looking for wrong server
**Solution:**
1. Click ⚙️ Settings
2. Clear and re-enter: `http://127.0.0.1:8001`
3. Click OK

### ❌ Extension doesn't appear in Chrome
**Problem:** Extension not loaded
**Solution:**
1. Go to `chrome://extensions/`
2. Enable Developer Mode (top-right toggle)
3. Click "Load unpacked"
4. Select `z:\AI-Learning-Companion\extension` folder

### ❌ "Cannot read property 'url' of undefined"
**Problem:** Chrome permissions issue
**Solution:**
1. Remove the extension
2. Go to `chrome://extensions/` → Remove Alexandria
3. Reload unpacked (see above)
4. Reload any open YouTube tabs

### ⏳ Summary/Export taking too long
**Problem:** Processing is slow
**Solution:**
- This is normal for first time (can take 30 seconds)
- Check backend console for errors
- Video length matters - longer videos take longer
- Check your internet connection

---

## 💡 Pro Tips & Tricks

### 🚀 Workflow Tips

1. **Batch Learning**
   - Open multiple YouTube videos
   - Generate summaries for all in background
   - Export all to Notion/Word
   - Study your organized notes

2. **Language Learning**
   - Watch videos in English
   - Translate summaries to your native language
   - Learn new vocabulary in context

3. **Content Curation**
   - Save important videos to library
   - Export collections for team sharing
   - Convert to different formats for different purposes

### ⚡ Keyboard Shortcuts
- **Alt+Shift+A** (if enabled): Quick open Alexandria
- Use Tab to navigate forms quickly

### 🎯 Best Practices

✅ **DO:**
- Generate summaries for long videos (saves time)
- Use Q&A for clarification
- Save important videos
- Export to organized locations

❌ **DON'T:**
- Close popup during processing
- Spam requests (they queue up)
- Use special characters in saved video titles
- Run extension without backend

---

## 📊 Extension Data & Privacy

### What Gets Saved?
- Your login credentials (encrypted JWT token)
- Video titles and URLs (stored in your library)
- Summaries (stored in database)

### What's Local?
- API URL preference (in browser storage)
- Session token (in browser storage)

### What's Cloud?
- All user data on your backend server
- No external services used

### Clear Data
To completely clear extension data:
1. Go to `chrome://extensions/`
2. Find Alexandria
3. Click "Remove"
4. Browser storage is automatically cleared

---

## 🆘 Getting More Help

### Check Backend Logs
```bash
# Terminal window running uvicorn shows:
# - Request logs
# - Errors and warnings
# - Processing status
```

### Enable Debug Mode
1. Open extension popup
2. Right-click → Inspect (opens DevTools)
3. Go to Console tab
4. See detailed logs and errors

### Test Endpoints Manually
```bash
# Test API is working:
curl http://127.0.0.1:8001/

# Should return available endpoints
```

---

## 🎓 Learning Resources

- **Frontend App**: `http://localhost:5174` (full UI with more options)
- **API Docs**: `http://127.0.0.1:8001/docs` (interactive Swagger docs)
- **Backend Code**: `z:\AI-Learning-Companion\backend\`

---

## ✨ What's New in v2.0

🔐 **User Accounts** - Save your progress across devices
🌍 **12 Languages** - Translate to Spanish, French, Chinese, Japanese, etc.
🎵 **Spotify & Podcasts** - Summarize audio content
📤 **Multi-Format Export** - Word, Markdown, Notion, Google Docs
📚 **Video Library** - Organize and access saved videos
💬 **Enhanced Q&A** - Better context understanding
⚡ **Performance** - Faster summaries and responses

---

**Enjoy learning with Alexandria! 🌿✨**

*Questions? Check the troubleshooting section or review backend logs.*
