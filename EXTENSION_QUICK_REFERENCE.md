# 🔌 Alexandria v2.0 Extension - Quick Start

## ⚡ 5-Minute Setup

### 1. Start Backend
```bash
cd z:\AI-Learning-Companion
uvicorn backend.main:app --port 8001
```
Wait for: `INFO: Uvicorn running on http://127.0.0.1:8001`

### 2. Load Extension
1. Go to `chrome://extensions/`
2. Enable **Developer Mode** (toggle)
3. Click **Load unpacked**
4. Select: `z:\AI-Learning-Companion\extension\`
5. ✅ Done!

### 3. Create Account
1. Click Alexandria icon 🌿
2. Click **Sign Up** tab
3. Enter: Username, Email, Password (min. 8 chars)
4. Click **Create Account**
5. ✅ Logged in!

---

## 🚀 Use Cases (In Extension)

### Summarize YouTube Video
1. Open any YouTube video
2. Click Alexandria icon
3. Click **⚡ Generate Summary**
4. ✅ Get summary in 10-30 seconds

### Ask Questions
1. Go to **💬 Q&A** tab
2. Type question
3. Click **Ask Question**
4. ✅ Get instant answer

### Export & Share
1. Go to **📤 Export** tab
2. Choose: Markdown / Word / Notion / Google Docs
3. Click **Export Summary**
4. ✅ Opens exported document

### Save for Later
1. Go to **📤 Export** tab
2. Click **💾 Save to Library**
3. ✅ Video saved

### Translate Summary
1. Go to **🌍 Languages** tab
2. Pick language (12 available)
3. Click **🔄 Translate**
4. ✅ Translation appears

### Add Spotify/Podcasts
1. Go to **🎵 Streaming** tab
2. Paste Spotify/Podcast URL
3. Click **➕ Add Content**
4. ✅ Ingested

### View Your Library
1. Go to **📚 Library** tab
2. Click **🔄 Refresh Library**
3. ✅ See all saved videos

---

## 🎯 Extension Features

| Tab | What It Does | How To Use |
|-----|-------------|-----------|
| 📝 Summary | Generate AI summaries | Click button, wait 10-30s |
| 💬 Q&A | Ask about video | Type question, hit ask |
| 📤 Export | Save in different formats | Choose format, export |
| 🌍 Languages | Translate to 12 languages | Pick language, translate |
| 🎵 Streaming | Add Spotify/Podcast | Paste URL, add |
| 📚 Library | View saved videos | Click refresh |

---

## 📝 UI Overview

```
┌─────────────────────────────────────┐
│  Alexandria v2.0  👤 john_doe      │  ← Header with user name
├─────────────────────────────────────┤
│ 📺 Current Video: [Video Title]     │  ← Shows current YouTube video
├─────────────────────────────────────┤
│ 📝│💬│📤│🌍│🎵│📚                  │  ← 6 Feature Tabs
├─────────────────────────────────────┤
│ [⚡ Generate Summary Button]         │  ← Active tab content
│ [Output area]                       │
├─────────────────────────────────────┤
│ ⚙️ │ Logout                          │  ← Footer buttons
└─────────────────────────────────────┘
```

---

## 🔑 Key Shortcuts

- **Right-click extension popup** → "Inspect" to see console logs
- **⚙️ Settings button** → Change API URL if needed
- **Logout** → Sign out and clear session

---

## ✅ Tested & Working

- ✅ YouTube video detection
- ✅ User authentication (login/signup)
- ✅ Summary generation
- ✅ Q&A functionality
- ✅ Multi-format export
- ✅ Language translation (12 languages)
- ✅ Spotify/Podcast ingestion
- ✅ Video library management
- ✅ Error handling & notifications

---

## ⚠️ Troubleshooting Quick Fixes

| Issue | Fix |
|-------|-----|
| "Not on YouTube video" | Open a YouTube video first |
| "Failed to connect" | Start backend: `uvicorn backend.main:app --port 8001` |
| "Login failed" | Check email/password, ensure password is 8+ chars |
| "API Base URL wrong" | Click ⚙️, enter `http://127.0.0.1:8001` |
| Extension missing | Go to `chrome://extensions/`, Load unpacked |

---

## 📊 What Happens Behind The Scenes

1. **You click Generate Summary**
   - Extension detects YouTube video ID
   - Sends to backend API
   - Backend extracts captions/audio
   - AI analyzes content
   - Returns summary

2. **You export to Notion**
   - Creates formatted document
   - Sends to Notion API (if configured)
   - Returns link to open document

3. **You translate**
   - Sends summary + target language
   - Google Gemini API translates
   - Returns translated text

4. **You add Spotify**
   - Detects if it's Spotify or podcast
   - Downloads audio
   - Transcribes with AssemblyAI
   - Processes like any video

---

## 🎓 Full Documentation

For complete details, see: **EXTENSION_USAGE_GUIDE.md**

---

**You're all set! Click the Alexandria icon and start summarizing! 🌿✨**
