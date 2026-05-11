import React, { useState, useEffect } from 'react';
import { Messaging, Logger } from '../shared/utils.js';
import './styles.css';

export default function SidePanelApp() {
  const [activeTab, setActiveTab] = useState('summary');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    loadAnalysis();
  }, []);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      // Get video ID from current context
      const response = await Messaging.send({ type: 'GET_ANALYSIS', payload: { videoId: 'current' } });
      
      if (response.success) {
        setAnalysis(response.data);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
      Logger.error('Load analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;

    try {
      const userMessage = { role: 'user', content: question };
      setMessages([...messages, userMessage]);
      setQuestion('');

      const response = await Messaging.send({
        type: 'ASK_QUESTION',
        payload: { videoId: 'current', question: question.trim() },
      });

      if (response.success) {
        const assistantMessage = { role: 'assistant', content: response.data.answer };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
      Logger.error('Ask error:', err);
    }
  };

  return (
    <div className="sidepanel-container">
      <div className="sidepanel-header">
        <h1>🧠 Alexandria AI</h1>
        <button className="refresh-btn" onClick={loadAnalysis} disabled={loading}>
          {loading ? '⏳' : '🔄'}
        </button>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          Summary
        </button>
        <button 
          className={`tab ${activeTab === 'qa' ? 'active' : ''}`}
          onClick={() => setActiveTab('qa')}
        >
          Q&A
        </button>
        <button 
          className={`tab ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => setActiveTab('timeline')}
        >
          Timeline
        </button>
      </div>

      {error && (
        <div className="error-box">
          {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="sidepanel-content">
        {activeTab === 'summary' && (
          <div className="summary-section">
            {loading ? (
              <div className="loading">Loading analysis...</div>
            ) : analysis ? (
              <>
                <div className="summary-block">
                  <h3>📖 Overall Summary</h3>
                  <p>{analysis.summary || 'Summary not available yet'}</p>
                </div>
                
                {analysis.topics && analysis.topics.length > 0 && (
                  <div className="topics-block">
                    <h3>📑 Topics</h3>
                    <ul>
                      {analysis.topics.map((topic, idx) => (
                        <li key={idx}>{topic}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            ) : (
              <p className="empty-state">No analysis available. Upload a video to get started.</p>
            )}
          </div>
        )}

        {activeTab === 'qa' && (
          <div className="qa-section">
            <div className="messages">
              {messages.length === 0 && (
                <p className="empty-state">Ask me anything about this video!</p>
              )}
              {messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <div className="message-content">{msg.content}</div>
                </div>
              ))}
            </div>

            <div className="qa-input">
              <input
                type="text"
                placeholder="Ask a question..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                disabled={loading}
              />
              <button
                className="send-btn"
                onClick={handleAskQuestion}
                disabled={loading || !question.trim()}
              >
                Send
              </button>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="timeline-section">
            {analysis?.timestamps && analysis.timestamps.length > 0 ? (
              <div className="timeline-list">
                {analysis.timestamps.map((ts, idx) => (
                  <div key={idx} className="timeline-item">
                    <span className="time">{ts.time}s</span>
                    <span className="label">{ts.label}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty-state">No timeline data available.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
