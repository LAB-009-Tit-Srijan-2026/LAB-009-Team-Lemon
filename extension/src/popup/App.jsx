import React, { useState, useEffect } from 'react';
import { Messaging, Logger } from '../shared/utils.js';
import './styles.css';

export default function PopupApp() {
  const [currentVideo, setCurrentVideo] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [question, setQuestion] = useState('');
  const [status, setStatus] = useState('idle');

  useEffect(() => {
    loadCurrentVideo();
  }, []);

  const loadCurrentVideo = async () => {
    try {
      setLoading(true);
      
      // Get current tab URL
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tabs.length > 0) {
        const tab = tabs[0];
        const url = tab.url;
        
        // Check if it's a YouTube, Vimeo, or video streaming URL
        if (url && (url.includes('youtube.com') || url.includes('youtu.be') || 
                    url.includes('vimeo.com') || url.includes('coursera.org') ||
                    url.includes('udemy.com'))) {
          setCurrentVideo({
            url: url,
            title: tab.title,
            videoId: url,
          });
          Logger.log('Video detected:', url);
        } else {
          setError('No video detected on this page. Please open a YouTube, Vimeo, Coursera, or Udemy video.');
        }
      }
    } catch (err) {
      setError(err.message);
      Logger.error('Load video error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    if (!currentVideo) return;
    
    try {
      setLoading(true);
      setStatus('processing');
      
      const response = await Messaging.send({
        type: 'INGEST_VIDEO',
        payload: { videoUrl: currentVideo.url },
      });

      if (response.success) {
        setStatus('ingesting');
        Logger.log('Ingestion started:', response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
      Logger.error('Ingest error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim() || !currentVideo) return;

    try {
      setLoading(true);
      const response = await Messaging.send({
        type: 'ASK_QUESTION',
        payload: {
          videoId: currentVideo.videoId,
          question: question.trim(),
        },
      });

      if (response.success) {
        Logger.log('Answer:', response.data);
        setQuestion('');
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
      Logger.error('Ask error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenFullPanel = async () => {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tabs.length > 0) {
      await chrome.sidePanel.open({ tabId: tabs[0].id });
    }
  };

  return (
    <div className="popup-container">
      <div className="popup-header">
        <h1>🧠 Alexandria AI</h1>
        <button 
          className="settings-btn" 
          onClick={() => chrome.runtime.openOptionsPage()}
          title="Settings"
        >
          ⚙️
        </button>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="popup-content">
        {!currentVideo ? (
          <div className="no-video">
            <p>No video detected on this page.</p>
            <p>Open a YouTube video or supported platform to get started.</p>
          </div>
        ) : (
          <>
            <div className="video-card">
              <h3>{currentVideo.title || 'Video'}</h3>
              <p className="video-url">{currentVideo.url}</p>
              <div className="video-status">
                Status: <span className="status-badge">{status}</span>
              </div>
            </div>

            <div className="action-buttons">
              <button 
                className="btn btn-primary"
                onClick={handleIngest}
                disabled={loading || status === 'ingesting'}
              >
                {loading ? 'Processing...' : '🚀 Analyze Video'}
              </button>
              <button 
                className="btn btn-secondary"
                onClick={handleOpenFullPanel}
              >
                📖 Full Analysis
              </button>
            </div>

            <div className="quick-question">
              <label>Quick Question:</label>
              <div className="question-input-group">
                <input
                  type="text"
                  placeholder="Ask about the video..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                  disabled={loading}
                />
                <button
                  className="btn btn-send"
                  onClick={handleAskQuestion}
                  disabled={loading || !question.trim()}
                >
                  →
                </button>
              </div>
            </div>
          </>
        )}
      </div>

      <div className="popup-footer">
        <small>v1.0.0</small>
      </div>
    </div>
  );
}
