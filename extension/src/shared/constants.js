// Shared constants for the extension
export const API_ENDPOINTS = {
  INGEST: '/ingest',
  INGEST_FILE: '/ingest-file',
  INGEST_STATUS: '/ingest-status',
  ASK: '/ask',
  ASK_STREAM: '/ask/stream',
  SUMMARY: '/summary',
  TOPIC_SUMMARIES: '/topic-summaries',
  LAST_MINUTES: '/last-minutes',
  TIMESTAMPS: '/timestamps',
  ANALYSIS: '/analysis',
  VIDEOS: '/videos',
  QUALITY: '/quality',
  HEALTH: '/health',
};

export const STORAGE_KEYS = {
  BACKEND_URL: 'backend_url',
  API_KEY: 'api_key',
  VIDEOS: 'videos',
  CURRENT_VIDEO: 'current_video',
  SETTINGS: 'settings',
};

export const DEFAULT_SETTINGS = {
  backend_url: 'http://localhost:8000',
  api_key: '',
  enable_notifications: true,
  max_history: 100,
  auto_ingest: false,
  theme: 'light',
};

export const VIDEO_PLATFORMS = {
  YOUTUBE: 'youtube',
  VIMEO: 'vimeo',
  COURSERA: 'coursera',
  UDEMY: 'udemy',
  GENERIC: 'generic',
};

export const INGEST_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

export const POLLING_INTERVAL = 2000; // 2 seconds
export const API_TIMEOUT = 30000; // 30 seconds
