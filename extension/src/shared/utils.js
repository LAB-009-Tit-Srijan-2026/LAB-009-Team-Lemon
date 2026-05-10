// Utility functions for API calls
import { API_ENDPOINTS, API_TIMEOUT } from './constants.js';

export class APIClient {
  constructor(baseURL, apiKey = '') {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const config = {
      ...options,
      headers,
      signal: AbortSignal.timeout(API_TIMEOUT),
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  async ingest(videoUrl) {
    return this.request(API_ENDPOINTS.INGEST, {
      method: 'POST',
      body: JSON.stringify({ video_url: videoUrl }),
    });
  }

  async getIngestStatus(jobId) {
    return this.request(`${API_ENDPOINTS.INGEST_STATUS}/${jobId}`);
  }

  async ask(videoId, question, sessionId = null) {
    return this.request(API_ENDPOINTS.ASK, {
      method: 'POST',
      body: JSON.stringify({ video_id: videoId, question, session_id: sessionId }),
    });
  }

  async getSummary(videoId) {
    return this.request(`${API_ENDPOINTS.SUMMARY}/${videoId}`);
  }

  async getAnalysis(videoId) {
    return this.request(`${API_ENDPOINTS.ANALYSIS}/${videoId}`);
  }

  async getTimestamps(videoId) {
    return this.request(`${API_ENDPOINTS.TIMESTAMPS}/${videoId}`);
  }

  async health() {
    return this.request('/health');
  }
}

// Storage utilities
export const Storage = {
  async get(keys) {
    return new Promise((resolve) => {
      chrome.storage.local.get(keys, resolve);
    });
  },

  async set(items) {
    return new Promise((resolve) => {
      chrome.storage.local.set(items, resolve);
    });
  },

  async remove(keys) {
    return new Promise((resolve) => {
      chrome.storage.local.remove(keys, resolve);
    });
  },

  async clear() {
    return new Promise((resolve) => {
      chrome.storage.local.clear(resolve);
    });
  },
};

// Message utilities
export const Messaging = {
  send(message) {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(message, (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(response);
        }
      });
    });
  },

  onMessage(callback) {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      Promise.resolve(callback(request, sender)).then(sendResponse).catch(console.error);
      return true; // Keep channel open for async response
    });
  },
};

// Video parser utilities
export const VideoParser = {
  extractYouTubeId(url) {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/)([0-9A-Za-z_-]{11})/,
      /(?:v=)([0-9A-Za-z_-]{11})/,
    ];
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  },

  detectVideoElement(document) {
    const videos = document.querySelectorAll('video');
    return videos.length > 0 ? videos[0] : null;
  },

  extractVideoInfo(document, url) {
    let title = document.title || 'Unknown Video';
    let videoId = this.extractYouTubeId(url);

    if (!videoId) {
      const titleEl = document.querySelector('h1') || document.querySelector('title');
      title = titleEl?.textContent || title;
    }

    return { title, videoId, url };
  },
};

// Logger utility
export const Logger = {
  log(...args) {
    console.log('[Learning Companion]', ...args);
  },

  error(...args) {
    console.error('[Learning Companion]', ...args);
  },

  warn(...args) {
    console.warn('[Learning Companion]', ...args);
  },
};
