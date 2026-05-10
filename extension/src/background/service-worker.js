import { APIClient, Storage, Messaging, Logger } from '../shared/utils.js';
import { STORAGE_KEYS, DEFAULT_SETTINGS, INGEST_STATUS, POLLING_INTERVAL } from '../shared/constants.js';

Logger.log('Background service worker loaded');

let apiClient = null;
const ingestJobs = {};

// Initialize API client on startup
chrome.runtime.onInstalled.addListener(async () => {
  Logger.log('Extension installed/updated');
  
  // Set default settings
  const stored = await Storage.get(STORAGE_KEYS.SETTINGS);
  if (!stored[STORAGE_KEYS.SETTINGS]) {
    await Storage.set({ [STORAGE_KEYS.SETTINGS]: DEFAULT_SETTINGS });
  }
  
  initializeAPIClient();
});

// Initialize API client from stored settings
async function initializeAPIClient() {
  const settings = await Storage.get(STORAGE_KEYS.SETTINGS);
  const currentSettings = settings[STORAGE_KEYS.SETTINGS] || DEFAULT_SETTINGS;
  
  apiClient = new APIClient(currentSettings.backend_url, currentSettings.api_key);
  Logger.log('API Client initialized with URL:', currentSettings.backend_url);
}

// Ensure API client is ready
async function ensureAPIClient() {
  if (!apiClient) {
    await initializeAPIClient();
  }
  return apiClient;
}

// Handle messages from content scripts and popup
Messaging.onMessage(async (request, sender) => {
  Logger.log('Background received message:', request.type);

  switch (request.type) {
    case 'HEALTH_CHECK':
      return handleHealthCheck();

    case 'INGEST_VIDEO':
      return handleIngestVideo(request.payload);

    case 'GET_INGEST_STATUS':
      return handleGetIngestStatus(request.payload.jobId);

    case 'ASK_QUESTION':
      return handleAskQuestion(request.payload);

    case 'GET_ANALYSIS':
      return handleGetAnalysis(request.payload.videoId);

    case 'SAVE_SETTINGS':
      return handleSaveSettings(request.payload);

    case 'GET_SETTINGS':
      return handleGetSettings();

    case 'OPEN_SIDEPANEL':
      return handleOpenSidePanel(sender.tab.id);

    default:
      return { success: false, error: 'Unknown message type' };
  }
});

// Health check
async function handleHealthCheck() {
  try {
    const client = await ensureAPIClient();
    const response = await client.health();
    return { success: true, data: response };
  } catch (error) {
    Logger.error('Health check failed:', error);
    return { success: false, error: error.message };
  }
}

// Ingest video
async function handleIngestVideo(payload) {
  try {
    const client = await ensureAPIClient();
    const response = await client.ingest(payload.videoUrl);
    
    // Store job info
    ingestJobs[response.job_id] = {
      ...response,
      startTime: Date.now(),
    };

    // Start polling for status
    pollIngestStatus(response.job_id);

    return { success: true, data: response };
  } catch (error) {
    Logger.error('Ingest failed:', error);
    return { success: false, error: error.message };
  }
}

// Get ingest status
async function handleGetIngestStatus(jobId) {
  try {
    const client = await ensureAPIClient();
    const response = await client.getIngestStatus(jobId);
    
    // Store job info
    ingestJobs[jobId] = response;

    return { success: true, data: response };
  } catch (error) {
    Logger.error('Get status failed:', error);
    return { success: false, error: error.message };
  }
}

// Poll ingest status
async function pollIngestStatus(jobId, attempt = 0) {
  const maxAttempts = 1800; // 1 hour with 2-second intervals

  if (attempt >= maxAttempts) {
    Logger.warn(`Job ${jobId} polling timeout`);
    ingestJobs[jobId] = { ...ingestJobs[jobId], status: INGEST_STATUS.FAILED };
    return;
  }

  try {
    const client = await ensureAPIClient();
    const response = await client.getIngestStatus(jobId);
    
    ingestJobs[jobId] = response;

    // Notify all listeners
    chrome.runtime.sendMessage({
      type: 'INGEST_STATUS_UPDATE',
      payload: response,
    }).catch(() => {
      // Ignore if no receiver
    });

    // Continue polling if not done
    if (response.status !== INGEST_STATUS.COMPLETED && response.status !== INGEST_STATUS.FAILED) {
      setTimeout(() => pollIngestStatus(jobId, attempt + 1), POLLING_INTERVAL);
    }
  } catch (error) {
    Logger.error('Poll status failed:', error);
    // Continue polling on error
    setTimeout(() => pollIngestStatus(jobId, attempt + 1), POLLING_INTERVAL);
  }
}

// Ask question
async function handleAskQuestion(payload) {
  try {
    const client = await ensureAPIClient();
    const response = await client.ask(payload.videoId, payload.question, payload.sessionId);
    return { success: true, data: response };
  } catch (error) {
    Logger.error('Ask failed:', error);
    return { success: false, error: error.message };
  }
}

// Get analysis
async function handleGetAnalysis(videoId) {
  try {
    const client = await ensureAPIClient();
    const response = await client.getAnalysis(videoId);
    return { success: true, data: response };
  } catch (error) {
    Logger.error('Get analysis failed:', error);
    return { success: false, error: error.message };
  }
}

// Save settings
async function handleSaveSettings(settings) {
  try {
    await Storage.set({ [STORAGE_KEYS.SETTINGS]: settings });
    await initializeAPIClient(); // Reinitialize with new settings
    return { success: true };
  } catch (error) {
    Logger.error('Save settings failed:', error);
    return { success: false, error: error.message };
  }
}

// Get settings
async function handleGetSettings() {
  try {
    const stored = await Storage.get(STORAGE_KEYS.SETTINGS);
    const settings = stored[STORAGE_KEYS.SETTINGS] || DEFAULT_SETTINGS;
    return { success: true, data: settings };
  } catch (error) {
    Logger.error('Get settings failed:', error);
    return { success: false, error: error.message };
  }
}

// Open side panel
async function handleOpenSidePanel(tabId) {
  try {
    await chrome.sidePanel.open({ tabId });
    return { success: true };
  } catch (error) {
    Logger.error('Open side panel failed:', error);
    return { success: false, error: error.message };
  }
}
