# AI Learning Companion - Browser Extension

A powerful browser extension for AI-driven video analysis, summarization, and interactive learning.

## Features

✨ **Core Features**
- 🎥 Automatic video detection (YouTube, Vimeo, Coursera, Udemy)
- 📋 AI-powered video summarization
- ❓ Interactive Q&A about video content
- ⏱️ Timeline navigation with timestamps
- 💬 Multi-turn conversation with session memory
- 🎯 One-click video ingestion
- 📊 Real-time ingestion progress tracking
- ⚙️ Customizable backend configuration

## Project Structure

```
extension/
├── public/                 # Static files
│   ├── manifest.json      # Extension manifest (Manifest v3)
│   ├── popup.html         # Popup UI
│   ├── sidepanel.html     # Full analysis panel
│   ├── options.html       # Settings page
│   └── icons/             # Extension icons
│
├── src/
│   ├── background/        # Service worker logic
│   ├── content/           # Content scripts
│   ├── popup/             # Popup UI components
│   ├── sidepanel/         # Side panel UI components
│   ├── options/           # Options page components
│   └── shared/            # Utilities and constants
│
├── webpack.config.js      # Build configuration
├── tsconfig.json          # TypeScript configuration
├── package.json           # Dependencies
└── README.md              # This file
```

## Development Setup

### Prerequisites
- Node.js 16+ and npm
- Modern browser (Chrome 96+, Edge 96+)
- Backend running (see backend README)

### Installation

1. **Clone the repository** (if needed)
   ```bash
   cd extension
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure backend URL**
   - Open `src/shared/constants.js`
   - Update `DEFAULT_SETTINGS.backend_url` if needed (default: `http://localhost:8000`)

### Development Build

```bash
# Build in watch mode for development
npm run dev

# Build once for production
npm run build

# Clean and rebuild
npm run build:clean
```

The built extension will be in the `dist/` folder.

## Loading Extension in Browser

### Chrome / Microsoft Edge

1. **Build the extension**
   ```bash
   npm run build
   ```

2. **Open the extension management page**
   - Chrome: Go to `chrome://extensions/`
   - Edge: Go to `edge://extensions/`

3. **Enable Developer Mode**
   - Toggle the "Developer mode" switch (top right corner)

4. **Load unpacked extension**
   - Click "Load unpacked"
   - Navigate to and select the `dist/` folder
   - The extension should now appear in your extensions list!

5. **Test the extension**
   - Go to a YouTube video page
   - Click the extension icon in the toolbar
   - Configure backend URL in settings if needed
   - Try analyzing a video!

## Configuration

### Backend URL Setup

1. **Click the extension icon** in your toolbar
2. **Click the ⚙️ settings button**
3. **Enter your backend URL**
   - Local development: `http://localhost:8000`
   - Remote server: `https://your-domain.com`
4. **Optionally add API key** if your backend requires authentication
5. **Click "Test Connection"** to verify
6. **Save Settings**

### Environment Variables

Create a `.env` file in the extension root:

```
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_BACKEND_API_KEY=your-api-key
REACT_APP_ENV=development
```

## Uploading to Chrome Web Store

### Step 1: Prepare Your Account

1. **Create a Google Developer account**
   - Visit: https://developer.chrome.com/docs/webstore
   - Sign in with your Google account
   - Accept the terms

2. **Register as a Chrome Web Store developer**
   - Pay the one-time registration fee ($5 USD)
   - Complete your developer information

### Step 2: Create Developer Assets

1. **Icon Pack** (in `public/icons/`)
   - 16x16 px - toolbar icon
   - 48x48 px - small extension icon
   - 128x128 px - app store listing
   - Format: PNG, JPG, or GIF

2. **Screenshots** (for store listing)
   - Create 3-5 screenshots (1280x800 px minimum)
   - Show key features (popup, side panel, settings)

3. **Promotional Image** (1400x560 px)
   - Optional: for featured listings

4. **Description & Details**
   ```
   Name: AI Learning Companion
   
   Short Description (132 chars max):
   AI-powered browser extension for video analysis and smart learning.
   
   Full Description:
   Transform your learning with AI-powered video analysis. Automatically 
   summarize videos, ask questions, and get intelligent insights. Works with 
   YouTube, Vimeo, Coursera, and more.
   
   Features:
   - Automatic video detection
   - AI-powered summaries
   - Interactive Q&A
   - Timeline navigation
   - Session memory
   - One-click analysis
   
   Languages: English (select primary)
   ```

### Step 3: Package the Extension

1. **Build production version**
   ```bash
   npm run build
   ```

2. **Create a ZIP file**
   - Right-click the `dist/` folder
   - On Windows: Send to → Compressed (zipped) folder
   - On macOS: Compress
   - Or use command line:
     ```bash
     # Windows PowerShell
     Compress-Archive -Path dist -DestinationPath extension.zip
     
     # Mac/Linux
     zip -r extension.zip dist/
     ```

### Step 4: Submit to Chrome Web Store

1. **Go to Chrome Web Store Dashboard**
   - https://chrome.google.com/webstore/devconsole

2. **Click "New Item"**

3. **Upload the ZIP file**
   - Select your `extension.zip`
   - Click "Upload"

4. **Fill Store Listing**
   - Title: AI Learning Companion
   - Category: Productivity → Other
   - Description: (Use template from Step 2)
   - Languages: English
   - Detailed description
   - Upload screenshots and icons

5. **Set Privacy Policy**
   - Provide privacy policy URL or write one:
     ```
     Your Privacy Policy
     
     This extension collects:
     - Video URLs (for processing)
     - Backend API communications
     - User settings (stored locally)
     - Session data (temporary)
     
     No personal data is sold or shared.
     All data is processed securely through your configured backend.
     ```

6. **Review & Publish**
   - Review all details
   - Accept Chrome Web Store terms
   - Click "Submit for review"

### Step 5: Review Process

- **Review time**: 1-3 days typically
- **You'll receive email** when approved or if changes needed
- **Once approved**: Listed on Chrome Web Store!

### Step 6: Post-Launch

1. **Share your store listing**
   - Get your extension URL from dashboard
   - Share: https://chrome.google.com/webstore/detail/[extension-id]

2. **Monitor reviews and feedback**
   - Respond to user reviews
   - Fix reported issues
   - Publish updates

3. **Update extension**
   - Make changes locally
   - Build: `npm run build`
   - Create new ZIP
   - Upload new version in dashboard
   - Updates roll out automatically to users

## Troubleshooting

### "Extension not working"
- Check backend URL in settings
- Verify backend is running
- Test connection button
- Check browser console for errors (F12)

### "Videos not detected"
- Make sure you're on a supported platform
- Try refreshing the page
- Check content script is loaded (should see 📚 button)

### "Build errors"
```bash
# Clear node_modules and reinstall
rm -r node_modules package-lock.json
npm install

# Clean and rebuild
npm run build:clean
```

### "Webpack errors"
- Make sure all files in `src/` are properly created
- Check for syntax errors in JavaScript files
- Run: `npm run lint`

## API Integration

The extension communicates with your backend via these endpoints:

- `POST /ingest` - Start video analysis
- `GET /ingest-status/{job_id}` - Check progress
- `POST /ask` - Ask question about video
- `GET /summary/{video_id}` - Get summary
- `GET /timestamps/{video_id}` - Get timeline
- `GET /health` - Health check

See [Backend README](../README.md) for detailed API documentation.

## Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 96+ | ✅ Supported |
| Edge | 96+ | ✅ Supported |
| Firefox | (future) | ⚠️ Planned (Manifest v2) |
| Safari | (future) | ⚠️ Planned |

## Performance Targets

- Popup load time: < 300ms
- Side panel load time: < 500ms
- Memory usage: < 100MB
- API response time: < 5s

## Security

- ✅ Manifest v3 with Content Security Policy
- ✅ HTTPS-only API communication
- ✅ No eval() or dynamic code execution
- ✅ Secure local storage
- ✅ Permission minimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

- 📧 Email: support@yourproject.com
- 🐛 Issues: https://github.com/your-repo/issues
- 💬 Discussions: https://github.com/your-repo/discussions

## License

MIT License - See LICENSE file

## Changelog

### v1.0.0 (Initial Release)
- Basic extension setup
- Video detection and analysis
- Q&A system
- Settings panel
- Chrome Web Store support

---

## Quick Command Reference

```bash
npm install              # Install dependencies
npm run dev             # Development build (watch mode)
npm run build           # Production build
npm run build:clean     # Clean and rebuild
npm run lint            # Lint code
npm run test            # Run tests
npm run test:watch      # Tests in watch mode
```

---

**Ready to launch?** Follow the steps in [Uploading to Chrome Web Store](#uploading-to-chrome-web-store) section above!
