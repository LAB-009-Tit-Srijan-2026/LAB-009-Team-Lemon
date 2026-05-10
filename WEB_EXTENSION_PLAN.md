# AI Learning Companion - Web Extension Planning Document

## Project Overview
A browser extension (Chrome/Edge/Firefox) that integrates with the AI Learning Companion backend to provide real-time video analysis, summarization, and Q&A capabilities directly from the browser.

---

## Table of Contents
1. [Extension Architecture](#extension-architecture)
2. [Core Features](#core-features)
3. [Technical Stack](#technical-stack)
4. [Development Steps](#development-steps)
5. [File Structure](#file-structure)
6. [UI/UX Design](#uiux-design)
7. [API Integration](#api-integration)
8. [Data Flow](#data-flow)
9. [Security & Privacy](#security--privacy)
10. [Testing & Deployment](#testing--deployment)

---

## Extension Architecture

### Components Overview
- **Content Script**: Runs in the context of web pages, detects videos, communicates with the backend
- **Background Service Worker**: Handles background tasks, manages state, processes API calls
- **Popup UI**: Quick access panel for users (icon click)
- **Side Panel**: Full-featured interface for analysis and Q&A
- **Options Page**: Settings and configuration
- **Manifest File**: Extension configuration and permissions

### Communication Flow
```
Web Page → Content Script → Background Worker → Backend API
                  ↓
            Popup/Side Panel UI ← Background Worker
```

---

## Core Features

### 1. Video Detection & Analysis
- **Automatic Detection**: Identify YouTube videos, embedded videos, LMS videos
- **One-Click Ingestion**: Send video to backend for processing
- **Status Tracking**: Show ingestion progress (downloading, transcribing, processing)
- **Visual Indicators**: Show when video is analyzed and ready

### 2. Summary Generation
- **Overall Summary**: Main content summary
- **Topic-Based Summaries**: Break down by topics/sections
- **Time-Based Summaries**: Last 5 minutes, custom time ranges
- **Quick Preview**: Fast summary while ingestion is ongoing

### 3. Interactive Q&A
- **Ask Questions**: Chat interface for questions about the video
- **Session Memory**: Keep conversation history within a session
- **Context-Aware Answers**: RAG-based responses with timestamps
- **Jump-to-Moment**: Click timestamps to jump to relevant video sections

### 4. Video Timeline
- **Visual Timeline**: Show chunks/segments with descriptions
- **Timestamp Navigation**: Click to jump to specific moments
- **Segment Exploration**: Browse through video content structure

### 5. Learning Tools
- **Quick Notes**: Save key points and timestamps
- **Highlight Export**: Export important sections
- **Study Guide**: AI-generated study questions and key takeaways
- **Session Export**: Export entire conversation for review

### 6. Settings & Management
- **Backend Configuration**: Set API endpoint, API key
- **Video History**: List of processed videos
- **Clear Cache**: Remove stored data
- **Privacy Options**: Control data retention
- **Keyboard Shortcuts**: Custom shortcuts for quick access

---

## Technical Stack

### Frontend Technologies
- **Language**: JavaScript/TypeScript
- **UI Framework**: React or Vue.js (lightweight, ~50-100KB)
- **Build Tool**: Webpack or Vite
- **Styling**: CSS-in-JS (Tailwind CSS or styled-components)
- **State Management**: Redux or Context API
- **Icons**: Feather Icons or Font Awesome

### Backend Integration
- **API Client**: Fetch API or Axios
- **Authentication**: API Key, Bearer Token
- **WebSocket**: Optional for real-time updates
- **Polling**: Fallback for ingestion status

### Storage
- **LocalStorage**: User preferences, settings
- **IndexedDB**: Larger data, conversation history
- **Chrome Storage API**: Extension-specific data sync

### Browser APIs
- `chrome.runtime`: Message passing, lifecycle
- `chrome.tabs`: Tab management, URL detection
- `chrome.storage`: Data persistence
- `chrome.contextMenus`: Right-click menu integration
- `chrome.sidePanel`: Side panel UI (Manifest v3)

---

## Development Steps

### Phase 1: Setup & Foundation (Week 1)
- [ ] Create manifest.json (Manifest v3)
- [ ] Set up project structure with Webpack/Vite
- [ ] Create TypeScript configuration
- [ ] Implement basic content script
- [ ] Implement background service worker
- [ ] Set up messaging system between components
- [ ] Create basic popup UI structure

### Phase 2: Core Features - Detection & Ingestion (Week 2)
- [ ] Implement YouTube video detection
- [ ] Support for other video platforms (Vimeo, embedded, LMS)
- [ ] Video metadata extraction (title, channel, duration)
- [ ] Backend connection and API testing
- [ ] Implement ingestion request workflow
- [ ] Create progress tracking UI
- [ ] Handle error states and retries

### Phase 3: Summary & Analysis UI (Week 3)
- [ ] Create side panel for full interface
- [ ] Build summary display component
- [ ] Implement topic-based summary view
- [ ] Create timeline/chunks visualization
- [ ] Add timestamp navigation
- [ ] Build quick notes feature
- [ ] Implement summary refresh mechanism

### Phase 4: Interactive Q&A System (Week 4)
- [ ] Create chat interface component
- [ ] Implement message send/receive
- [ ] Build conversation history display
- [ ] Add session management
- [ ] Implement typing indicators
- [ ] Add error handling for failed questions
- [ ] Create session persistence

### Phase 5: Advanced Features (Week 5)
- [ ] Add keyboard shortcuts
- [ ] Implement right-click context menu
- [ ] Build settings/options page
- [ ] Create video history view
- [ ] Add export functionality
- [ ] Implement data cleanup/cache management
- [ ] Add user preferences persistence

### Phase 6: Testing & Polish (Week 6)
- [ ] Unit testing (Jest)
- [ ] Integration testing
- [ ] E2E testing with test videos
- [ ] Performance optimization
- [ ] Security audit
- [ ] Accessibility review
- [ ] Browser compatibility testing

### Phase 7: Deployment (Week 7)
- [ ] Chrome Web Store submission
- [ ] Edge Add-ons submission
- [ ] Firefox Add-ons submission
- [ ] Create documentation and guides
- [ ] Set up support channels
- [ ] Monitor and gather feedback

---

## File Structure

```
extension/
├── public/
│   ├── manifest.json              # Extension configuration
│   ├── icons/
│   │   ├── icon-16.png           # Small icon
│   │   ├── icon-48.png           # Small icon
│   │   ├── icon-128.png          # Store icon
│   │   └── icon-256.png          # Large icon
│   └── _locales/
│       └── en/
│           └── messages.json      # i18n strings
│
├── src/
│   ├── manifest.ts               # Manifest generation (if using TypeScript)
│   ├── background/
│   │   ├── index.ts              # Service worker entry
│   │   ├── api-client.ts         # Backend API calls
│   │   ├── message-handler.ts    # Message routing
│   │   ├── job-manager.ts        # Track ingestion jobs
│   │   └── storage-manager.ts    # Data persistence
│   │
│   ├── content/
│   │   ├── index.ts              # Content script entry
│   │   ├── video-detector.ts     # Detect videos on pages
│   │   ├── video-injector.ts     # Inject UI elements
│   │   └── page-parser.ts        # Extract video metadata
│   │
│   ├── popup/
│   │   ├── index.tsx             # Popup entry point
│   │   ├── App.tsx               # Popup main component
│   │   ├── components/
│   │   │   ├── VideoCard.tsx
│   │   │   ├── AnalysisStatus.tsx
│   │   │   └── QuickActions.tsx
│   │   └── styles.css
│   │
│   ├── sidepanel/
│   │   ├── index.tsx             # Side panel entry point
│   │   ├── App.tsx               # Side panel main component
│   │   ├── pages/
│   │   │   ├── SummaryPage.tsx   # Display summaries
│   │   │   ├── QAPage.tsx        # Q&A interface
│   │   │   ├── TimelinePage.tsx  # Timeline view
│   │   │   ├── HistoryPage.tsx   # Video history
│   │   │   └── SettingsPage.tsx  # Settings
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── SummaryDisplay.tsx
│   │   │   ├── Timeline.tsx
│   │   │   ├── IngestionProgress.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   └── styles/
│   │       ├── main.css
│   │       ├── components.css
│   │       └── responsive.css
│   │
│   ├── options/
│   │   ├── index.tsx             # Options page entry
│   │   ├── App.tsx               # Settings component
│   │   ├── pages/
│   │   │   ├── GeneralSettings.tsx
│   │   │   ├── APISettings.tsx
│   │   │   ├── PrivacySettings.tsx
│   │   │   └── KeyboardShortcuts.tsx
│   │   └── styles.css
│   │
│   ├── shared/
│   │   ├── types.ts              # TypeScript interfaces
│   │   ├── constants.ts          # Configuration constants
│   │   ├── utils/
│   │   │   ├── api-client.ts     # API request utilities
│   │   │   ├── storage.ts        # Storage helpers
│   │   │   ├── message.ts        # Message passing utilities
│   │   │   ├── video-parser.ts   # Extract video IDs
│   │   │   ├── time-formatter.ts # Format timestamps
│   │   │   └── logger.ts         # Logging utilities
│   │   └── hooks/
│   │       ├── useVideoState.ts
│   │       ├── useBackendAPI.ts
│   │       ├── useStorage.ts
│   │       └── useMessages.ts
│   │
│   └── assets/
│       ├── images/
│       └── fonts/
│
├── tests/
│   ├── unit/
│   │   ├── video-detector.test.ts
│   │   ├── api-client.test.ts
│   │   └── storage-manager.test.ts
│   ├── integration/
│   │   ├── extension-flow.test.ts
│   │   └── backend-integration.test.ts
│   └── fixtures/
│       ├── mock-videos.json
│       └── mock-responses.json
│
├── webpack.config.js            # Webpack configuration
├── tsconfig.json                # TypeScript config
├── .env.example                 # Environment variables
├── package.json                 # Dependencies
├── README.md                    # Extension documentation
└── DEVELOPMENT.md              # Development guide

```

---

## UI/UX Design

### 1. Popup UI (Quick Access)
```
┌─────────────────────────────┐
│ 🎓 Learning Companion       │ [⚙️]
├─────────────────────────────┤
│                             │
│ 📺 Current Video            │
│ ├─ Title: "Learn Python..." │
│ ├─ Status: Analyzing...     │
│ └─ [View Full Analysis]     │
│                             │
│ 📋 Latest Summary           │
│ "This video covers..."      │
│ [Read More]                 │
│                             │
│ ❓ Quick Question?          │
│ [__________________] [Send] │
│                             │
│ [📜 Full Panel] [History]   │
└─────────────────────────────┘
```

### 2. Side Panel UI (Full Featured)
```
┌──────────────────────────┐
│ 📚 Learning Analysis     │
├──────────────────────────┤
│ [Summary] [Q&A] [Time... │
├──────────────────────────┤
│                          │
│ 📺 "Learn Python ep 34"  │
│                          │
│ ■■■■■□□□□ 60%           │
│ Analyzing video...       │
│                          │
├──────────────────────────┤
│ 📖 SUMMARY              │
│                          │
│ This video teaches:     │
│ • Decorators            │
│ • Generators            │
│ • Best practices        │
│                          │
│ [Full Summary] [Topics] │
├──────────────────────────┤
│ 💡 KEY POINTS           │
│ 1. @ syntax for...      │
│ 2. yield keyword...     │
│ [Save Note]             │
│                          │
│ [Jump to 5:30]          │
└──────────────────────────┘
```

### 3. Q&A Interface
```
┌──────────────────────────┐
│ ❓ Ask Anything          │
├──────────────────────────┤
│                          │
│ 👤 You: "What is..."    │
│                          │
│ 🤖 Assistant:           │
│ "Based on the video..." │
│ [Jump to 3:45]          │
│                          │
│ 📝 Input field:         │
│ [_________________] [→] │
│                          │
│ [Save] [Export] [Clear] │
└──────────────────────────┘
```

### 4. Settings Page
```
┌──────────────────────────┐
│ ⚙️ Settings             │
├──────────────────────────┤
│ [General] [API] [Privacy]│
├──────────────────────────┤
│                          │
│ 🔗 API SETTINGS         │
│                          │
│ Backend URL:            │
│ [_____________________] │
│                          │
│ API Key:                │
│ [_____________________] │
│                          │
│ ☑️ Enable ChromaDB      │
│                          │
│ [Test Connection]       │
│ [Save] [Reset to Def]   │
└──────────────────────────┘
```

---

## API Integration

### Backend Endpoints Used
```
POST   /ingest              - Start video ingestion
POST   /ingest-file         - Upload file
GET    /ingest-status/{id}  - Check progress
POST   /ask                 - Ask question
POST   /ask/stream          - Stream answer
GET    /summary/{video_id}  - Get overall summary
GET    /topic-summaries/{id}- Get topic breakdown
GET    /last-minutes/{id}   - Get time-based summary
GET    /timestamps/{id}     - Get video chunks
GET    /analysis/{id}       - Complete analysis
GET    /videos              - List all videos
POST   /videos/{id}/clear   - Delete video data
GET    /quality/{id}        - Quality report
GET    /health              - Health check
```

### Request/Response Examples

**Ingest Video**
```json
Request:
POST /ingest
{
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}

Response:
{
  "job_id": "uuid",
  "video_id": "uuid",
  "status": "processing",
  "progress": 5,
  "step_name": "Starting..."
}
```

**Ask Question**
```json
Request:
POST /ask
{
  "video_id": "uuid",
  "question": "What is the main topic?",
  "session_id": "uuid"
}

Response:
{
  "answer": "The main topic is...",
  "timestamps": [
    {"time": 0.5, "label": "Introduction"},
    {"time": 45.3, "label": "Relevant section"}
  ],
  "session_id": "uuid"
}
```

---

## Data Flow

### 1. User Discovers Video
```
1. User opens YouTube/LMS page
2. Content script detects video
3. Extension icon highlights in toolbar
4. Visual indicator appears on video (optional)
```

### 2. Ingestion Workflow
```
User clicks "Analyze"
    ↓
Content Script sends video URL
    ↓
Background Worker creates job
    ↓
Backend processes video (async)
    ↓
Polling status every 2-5 seconds
    ↓
UI updates with progress (15%, 50%, 100%)
    ↓
Side panel shows summary when ready
```

### 3. Q&A Workflow
```
User types question + hits Send
    ↓
Message → Background Worker
    ↓
API call to /ask endpoint
    ↓
Stream response character by character (optional)
    ↓
Display answer with timestamps
    ↓
Store in conversation history
    ↓
User can click timestamps to jump
```

### 4. Storage Hierarchy
```
SessionStorage (temporary)
├─ Current video analysis
└─ Active conversation

LocalStorage (persistent, small)
├─ Settings & preferences
├─ API endpoint configuration
└─ Keyboard shortcuts

IndexedDB (persistent, large)
├─ Video history (100 entries max)
├─ Conversation archives
├─ Cached summaries
└─ User notes
```

---

## Security & Privacy

### API Security
- [ ] HTTPS only for API calls
- [ ] API key management (secure storage)
- [ ] Token refresh mechanism
- [ ] CORS handling
- [ ] Rate limiting
- [ ] Request signing (optional)

### Data Privacy
- [ ] No persistent logging of video content
- [ ] User control over data retention
- [ ] Clear cache functionality
- [ ] Option to disable video history
- [ ] Privacy policy compliance (GDPR, CCPA)
- [ ] User consent for data collection

### Browser Security
- [ ] Content Security Policy (CSP)
- [ ] No eval() or dynamic code execution
- [ ] Sanitized DOM insertions
- [ ] XSS protection
- [ ] Permission minimization
- [ ] Secure background worker

### Permissions (Minimal)
```json
"permissions": [
  "storage",
  "tabs",
  "sidePanel"
],
"host_permissions": [
  "https://www.youtube.com/*",
  "https://*.vimeo.com/*",
  "<backend-url>"
],
"optional_permissions": [
  "contextMenus"
]
```

---

## Testing & Deployment

### Testing Strategy

**Unit Tests**
- Video detection/parsing functions
- Storage utilities
- Time formatting utilities
- Message handling logic

**Integration Tests**
- Backend API integration
- Storage operations
- Message passing flow
- Error handling

**E2E Tests**
- Full workflow (detect → ingest → summarize → Q&A)
- Different video platforms
- Error scenarios
- Performance under load

### Test Videos
```
YouTube: Mix of lengths (5min, 30min, 2hr)
Vimeo: Various quality levels
LMS: Canvas, Blackboard, Moodle
```

### Performance Targets
- Popup load time: < 300ms
- Side panel load time: < 500ms
- API response time: < 5s for questions
- Memory usage: < 100MB

### Browser Support
- ✅ Chrome 96+ (Manifest v3)
- ✅ Edge 96+
- ⚠️ Firefox (Manifest v2 - future v3)
- ⚠️ Safari (WebExtensions API support)

### Deployment Checklist
- [ ] All tests passing (100% coverage for core modules)
- [ ] Performance benchmarks met
- [ ] Security audit completed
- [ ] Accessibility (WCAG 2.1 AA) verified
- [ ] Localization (at least English + 2 languages)
- [ ] Documentation complete
- [ ] Privacy policy written
- [ ] Terms of service drafted
- [ ] Store listings prepared

### Store Submissions
**Chrome Web Store**
- Category: Productivity
- Description, screenshots, privacy policy
- Review time: 1-3 days typically

**Edge Add-ons**
- Similar process to Chrome
- May require additional security review

**Firefox Add-ons**
- Manifest v2 compatibility needed for now
- Community review available

---

## Configuration & Environment

### .env File
```
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_BACKEND_API_KEY=your-api-key
REACT_APP_DEFAULT_TIMEOUT=30000
REACT_APP_POLLING_INTERVAL=3000
REACT_APP_MAX_HISTORY_ITEMS=100
REACT_APP_ENV=development
```

### Build Commands
```bash
npm run dev              # Development mode
npm run build            # Production build
npm run test             # Run tests
npm run test:watch       # Watch mode
npm run lint             # Lint code
npm run build:clean      # Clean build
```

---

## Future Enhancements

### Phase 2 Features
- [ ] Browser bookmarks integration
- [ ] Playlist analysis (analyze multiple videos)
- [ ] Custom themes and UI customization
- [ ] Voice commands for Q&A
- [ ] Offline mode with cached data
- [ ] Collaborative features (share notes)
- [ ] Email/Slack notifications

### Phase 3 Features
- [ ] ML-based content recommendations
- [ ] Video recommendations based on history
- [ ] Quiz/test generation
- [ ] Study plan generation
- [ ] Mobile app companion
- [ ] Browser sync across devices
- [ ] API for third-party developers

### Phase 4 Features
- [ ] AI-powered transcription corrections
- [ ] Real-time translation
- [ ] Accessibility features (captions, descriptions)
- [ ] Advanced analytics dashboard
- [ ] Integration with note-taking apps (Notion, OneNote)
- [ ] Enterprise licensing

---

## Success Metrics

### User Adoption
- 1,000 installs in first month
- 10,000 installs in first 6 months
- 4.5+ star rating on stores
- < 5% uninstall rate

### Engagement
- 30% daily active users
- 5+ average videos analyzed per user
- 10+ average questions per session
- 80% feature discoverability

### Performance
- < 100ms popup load time
- < 50ms API response time
- 99.9% uptime for backend
- < 0.1% error rate

---

## References & Resources

### Browser Extension APIs
- Chrome DevTools: https://developer.chrome.com/docs/extensions/
- WebExtensions API: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions

### Related Technologies
- Manifest v3: https://developer.chrome.com/docs/extensions/mv3/
- Service Workers: https://developer.chrome.com/docs/extensions/mv3/service_workers/
- React: https://react.dev
- TypeScript: https://www.typescriptlang.org

### Similar Projects
- YouTube Video Summarizer extensions
- LearningStudio companions
- Video note-taking tools
- RAG-based analysis tools

---

## Conclusion

This web extension transforms the AI Learning Companion backend into an accessible, user-friendly tool directly integrated into the browser. By following this plan, we can create a polished, feature-rich extension that enhances users' learning experience across multiple video platforms.

**Total Estimated Development Time**: 6-8 weeks (including testing and deployment)

**Team Requirements**: 1-2 frontend developers, 1 QA engineer, 1 product manager
