# Frontend Integration Guide - AI Learning Companion Backend

Quick reference for integrating the backend API into the LMS frontend.

## 🚀 Backend Server

**Start Command:**
```powershell
cd z:\AI-Learning-Companion
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**Base URL:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs` (Swagger UI)

---

## 📋 Core Workflows

### Workflow 1: Upload & Ask Questions

```javascript
// 1. Ingest a YouTube video
const ingestResponse = await fetch('http://localhost:8000/ingest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_url: 'https://www.youtube.com/watch?v=VIDEO_ID'
  })
});
const { video_id } = await ingestResponse.json();

// 2. Ask a question
const askResponse = await fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_id,
    question: 'What is the main topic?',
    session_id: 'optional-session-123' // For multi-turn conversations
  })
});
const { answer, timestamps } = await askResponse.json();

// 3. Use timestamps to jump in video player
player.seek(timestamps[0]); // [start_time, end_time]
```

### Workflow 2: Stream Real-Time Responses

```javascript
// Stream the response character by character
const streamResponse = await fetch('http://localhost:8000/ask/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_id,
    question: 'Explain the concept',
    session_id: 'session-123'
  })
});

const reader = streamResponse.body.getReader();
const decoder = new TextDecoder();
let fullAnswer = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const line = decoder.decode(value);
  const json = JSON.parse(line);
  
  if (json.chunk) {
    fullAnswer += json.chunk;
    updateUIWithChunk(json.chunk); // Real-time display
  }
  if (json.done) {
    console.log('Timestamps:', json.timestamps);
  }
}
```

### Workflow 3: Display All Summary Types

```javascript
// Get overall summary
const summaryResponse = await fetch(`http://localhost:8000/summary/${video_id}`);
const { summary: overallSummary } = await summaryResponse.json();

// Get topic-wise summaries
const topicsResponse = await fetch(`http://localhost:8000/topic-summaries/${video_id}`);
const { topics } = await topicsResponse.json();
// topics = [{ topic, summary, timestamp }, ...]

// Get last 5 minutes summary
const last5Response = await fetch(`http://localhost:8000/last-minutes/${video_id}?minutes=5`);
const { summary: lastMinutesSummary, timestamp } = await last5Response.json();

// Display each in your UI
displayOverallSummary(overallSummary);
displayTopics(topics);
displayTimedSummary(lastMinutesSummary, timestamp);
```

### Workflow 4: Jump-to-Moment Navigation

```javascript
// Get all timestamps for timeline/buttons
const timestampsResponse = await fetch(`http://localhost:8000/timestamps/${video_id}`);
const { timestamps } = await timestampsResponse.json();
// timestamps = [{ time: 0, label: "Chunk 1", duration: 25 }, ...]

// Create clickable timeline
timestamps.forEach(chunk => {
  const button = document.createElement('button');
  button.textContent = `${chunk.label} (${formatTime(chunk.time)})`;
  button.onclick = () => player.seek(chunk.time);
  timelineContainer.appendChild(button);
});

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}
```

---

## 🔌 API Reference

### All Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/ping` | Health check |
| `GET` | `/health` | Detailed health |
| `GET` | `/` | API overview |
| `POST` | `/ingest` | Ingest video |
| `POST` | `/ask` | Ask question (standard) |
| `POST` | `/ask/stream` | Ask question (streaming) |
| `GET` | `/summary/{id}` | Overall summary |
| `GET` | `/topic-summaries/{id}` | Topic summaries |
| `GET` | `/last-minutes/{id}?minutes=5` | Time-based summary |
| `GET` | `/timestamps/{id}` | Timestamps for timeline |

### Response Formats

**Success Response:**
```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "answer": "The main topic is...",
  "timestamps": [120.5, 185.3],
  "session_id": "optional-session-123",
  "status": "success"
}
```

**Error Response:**
```json
{
  "detail": "Descriptive error message"
}
```

---

## 🎨 UI/UX Recommendations

### 1. Question Input
- Text input field with send button
- Optional session_id selector for continuing conversations
- Show loading spinner while waiting for `/ask` response

### 2. Streaming Display
- Display answer text character-by-character as it streams
- Show final timestamp highlights
- Automatically jump video player to relevant timestamp

### 3. Summaries Panel
- Tabs: Overall | Topics | Last 5 Min
- Each topic clickable to jump to that moment
- Display timestamps in HH:MM:SS format

### 4. Timeline
- Visual timeline with chunks as buttons/markers
- Click any chunk to jump in video
- Show chunk labels (Chunk 1, Chunk 2, etc)

### 5. Session Management
- Generate session_id on page load: `session_${Date.now()}`
- Pass to all `/ask` and `/ask/stream` requests
- Enables multi-turn conversations within same session

---

## 🧪 Testing in Browser Console

```javascript
// Quick test
const vid = await fetch('http://localhost:8000/ingest', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_url: 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
  })
}).then(r => r.json());

const ans = await fetch('http://localhost:8000/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_id: vid.video_id,
    question: 'What is this about?'
  })
}).then(r => r.json());

console.log('Answer:', ans.answer);
console.log('Jump to:', ans.timestamps);
```

---

## 💡 Error Handling

```javascript
async function safeFetch(endpoint, options) {
  try {
    const response = await fetch(`http://localhost:8000${endpoint}`, options);
    if (!response.ok) {
      const error = await response.json();
      console.error('API Error:', error.detail);
      return null;
    }
    return await response.json();
  } catch (err) {
    console.error('Network error:', err.message);
    return null;
  }
}
```

---

## 🔐 CORS & Security

- Backend allows all origins (`*`)
- No authentication required for MVP
- For production:
  - Restrict `allow_origins` to your domain
  - Add authentication (JWT, OAuth)
  - Implement rate limiting
  - Add HTTPS

---

## 📝 Notes for Frontend Dev

- All timestamps are in **seconds** (float)
- Session memory is in-memory (cleared on server restart)
- YouTube videos must have public captions available
- If caption fetch fails, demo transcript is used
- Streaming endpoint returns NDJSON (newline-delimited JSON)

---

## 🚀 Ready to Build!

Frontend repo: (when created)  
Backend: `z:\AI-Learning-Companion`  
Docs: `http://localhost:8000/docs`

Happy coding!
