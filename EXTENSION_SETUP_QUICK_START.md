# Quick Start Guide - Building & Running the Extension

## ⚡ 30-Second Setup

```bash
# 1. Navigate to extension folder
cd extension

# 2. Install dependencies
npm install

# 3. Build for development (with watch mode)
npm run dev

# OR build once for production
npm run build
```

**The extension is now ready in the `dist/` folder!**

---

## 🚀 Loading into Your Browser (5 minutes)

### For Chrome or Edge:

1. **Open extension management page**
   ```
   Chrome: chrome://extensions/
   Edge:   edge://extensions/
   ```

2. **Enable Developer Mode** (top right toggle)

3. **Click "Load unpacked"** button

4. **Select the `dist/` folder** from the extension directory

5. **Extension is now loaded!** 🎉
   - You should see it in the toolbar
   - Click to open the popup
   - Pin it for easy access

---

## ⚙️ Configure Backend

1. **Click extension icon** in toolbar
2. **Click ⚙️ settings button** (top right)
3. **Set Backend URL**:
   - Local: `http://localhost:8000`
   - Remote: `https://your-server.com`
4. **Add API Key** (if required)
5. **Click "Test Connection"** ✓
6. **Save Settings**

---

## 📹 Test It Out

1. Go to any **YouTube video**
2. Click **extension icon** → **🚀 Analyze Video**
3. Watch the ingestion progress bar
4. Once ready, see:
   - 📖 Summary tab (video summary)
   - ❓ Q&A tab (ask questions)
   - ⏱️ Timeline tab (jump to moments)

---

## 📤 Upload to Chrome Web Store (Optional)

### Step-by-step:

#### 1. Create Chrome Developer Account
- Go to: https://developer.chrome.com/docs/webstore
- Sign in with Google
- Pay $5 registration fee

#### 2. Build & Package
```bash
# Build production version
npm run build

# Create ZIP file (Windows PowerShell)
Compress-Archive -Path dist -DestinationPath extension.zip

# OR on Mac/Linux
zip -r extension.zip dist/
```

#### 3. Upload to Store
- Go to: https://chrome.google.com/webstore/devconsole
- Click "New Item"
- Upload `extension.zip`
- Fill in store details:
  - Title: AI Learning Companion
  - Category: Productivity
  - Description: (see README.md)
  - Add screenshots
  - Add privacy policy
- Submit for review (1-3 days)

#### 4. Share
Once approved, share your store link:
```
https://chrome.google.com/webstore/detail/[your-extension-id]
```

---

## 📋 File Structure

```
extension/
├── dist/                    ← Built extension (load this)
├── src/
│   ├── popup/              ← Quick popup UI
│   ├── sidepanel/          ← Full analysis panel
│   ├── background/         ← Service worker
│   ├── content/            ← Video detection
│   ├── options/            ← Settings page
│   └── shared/             ← Utilities
├── public/
│   ├── manifest.json       ← Extension config
│   ├── popup.html          ← Popup template
│   ├── sidepanel.html      ← Panel template
│   └── icons/              ← Extension icons
├── package.json
├── webpack.config.js       ← Build config
└── README.md               ← Full documentation
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Extension not showing in toolbar | Clear build, rebuild, reload browser |
| Backend connection fails | Check URL in settings, ensure backend is running |
| Videos not detected | Verify supported platform (YouTube, Vimeo, etc.) |
| Build errors | Run `npm install` again, check node version (16+) |
| Can't load unpacked | Enable Developer Mode first |

---

## 💡 Next Steps

1. ✅ **Build locally** - Test in development
2. ✅ **Test with videos** - Try YouTube, Vimeo, etc.
3. ✅ **Configure settings** - Set your backend URL
4. ✅ **Submit to store** - Make it available to everyone
5. ✅ **Gather feedback** - Improve based on reviews

---

## 🔗 Useful Links

- **Chrome Extension Docs**: https://developer.chrome.com/docs/extensions/mv3/
- **Manifest v3 Guide**: https://developer.chrome.com/docs/extensions/mv3/manifest/
- **Web Store Console**: https://chrome.google.com/webstore/devconsole
- **Backend Setup**: See main project README.md

---

**Questions?** Check `README.md` in the extension folder for full documentation!
