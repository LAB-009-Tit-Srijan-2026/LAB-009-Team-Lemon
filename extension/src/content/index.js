import { Messaging, Logger, VideoParser, Storage } from '../shared/utils.js';
import { STORAGE_KEYS } from '../shared/constants.js';

Logger.log('Content script loaded');

// Detect if video is on the page and notify background
async function detectAndNotifyVideo() {
  const url = window.location.href;
  const videoInfo = VideoParser.extractVideoInfo(document, url);

  if (videoInfo.videoId) {
    Logger.log('Video detected:', videoInfo);
    
    // Send message to background
    await Messaging.send({
      type: 'VIDEO_DETECTED',
      payload: videoInfo,
    });

    // Add visual indicator (optional)
    addVideoIndicator();
  }
}

// Add a subtle indicator that extension is active
function addVideoIndicator() {
  const indicator = document.createElement('div');
  indicator.id = 'alexandria-ai-indicator';
  indicator.title = 'Alexandria AI - Click to analyze';
  indicator.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 10000;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    font-size: 28px;
    user-select: none;
    transition: all 0.3s ease;
  `;
  indicator.textContent = '🧠';
  
  indicator.addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'OPEN_SIDEPANEL' });
  });

  indicator.addEventListener('mouseenter', () => {
    indicator.style.transform = 'scale(1.12)';
    indicator.style.boxShadow = '0 8px 28px rgba(102, 126, 234, 0.5)';
  });

  indicator.addEventListener('mouseleave', () => {
    indicator.style.transform = 'scale(1)';
    indicator.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.4)';
  });

  document.body.appendChild(indicator);
}

// Listen for messages from background/popup
Messaging.onMessage(async (request, sender) => {
  Logger.log('Content received:', request);

  switch (request.type) {
    case 'GET_VIDEO_INFO':
      const url = window.location.href;
      const info = VideoParser.extractVideoInfo(document, url);
      return { success: true, data: info };

    case 'INJECT_CONTROLS':
      addVideoIndicator();
      return { success: true };

    default:
      return { success: false, error: 'Unknown message type' };
  }
});

// Detect video when page loads
detectAndNotifyVideo();

// Also detect on dynamic changes
window.addEventListener('load', detectAndNotifyVideo);
document.addEventListener('urlchange', detectAndNotifyVideo);
