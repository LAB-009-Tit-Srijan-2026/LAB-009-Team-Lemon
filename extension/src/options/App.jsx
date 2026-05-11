import React, { useState, useEffect } from 'react';
import { Messaging, Logger, Storage } from '../shared/utils.js';
import { STORAGE_KEYS, DEFAULT_SETTINGS } from '../shared/constants.js';
import './styles.css';

export default function OptionsApp() {
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [saved, setSaved] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await Messaging.send({ type: 'GET_SETTINGS' });
      if (response.success) {
        setSettings(response.data);
      }
    } catch (err) {
      Logger.error('Load settings error:', err);
    }
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    try {
      const response = await Messaging.send({
        type: 'SAVE_SETTINGS',
        payload: settings,
      });

      if (response.success) {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
      }
    } catch (err) {
      Logger.error('Save settings error:', err);
    }
  };

  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setTestResult(null);

      const response = await Messaging.send({ type: 'HEALTH_CHECK' });

      if (response.success) {
        setTestResult({ success: true, message: 'Connection successful! ✓' });
      } else {
        setTestResult({ success: false, message: `Error: ${response.error}` });
      }
    } catch (err) {
      setTestResult({ success: false, message: `Error: ${err.message}` });
    } finally {
      setTesting(false);
    }
  };

  const handleReset = () => {
    if (confirm('Reset to default settings?')) {
      setSettings(DEFAULT_SETTINGS);
    }
  };

  return (
    <div className="options-container">
      <div className="options-header">
        <h1>🧠 Alexandria AI Settings</h1>
        <p>Configure your intelligent learning companion</p>
      </div>

      <div className="options-content">
        <div className="settings-section">
          <h2>Backend Configuration</h2>
          
          <div className="form-group">
            <label htmlFor="backend-url">Backend URL</label>
            <input
              id="backend-url"
              type="text"
              value={settings.backend_url}
              onChange={(e) => handleChange('backend_url', e.target.value)}
              placeholder="http://localhost:8000"
            />
            <small>The API endpoint where your backend is running</small>
          </div>

          <div className="form-group">
            <label htmlFor="api-key">API Key (optional)</label>
            <input
              id="api-key"
              type="password"
              value={settings.api_key}
              onChange={(e) => handleChange('api_key', e.target.value)}
              placeholder="Leave blank if not required"
            />
            <small>Authentication key for your backend API</small>
          </div>

          <div className="button-group">
            <button 
              className="btn btn-test"
              onClick={handleTestConnection}
              disabled={testing}
            >
              {testing ? 'Testing...' : '🔌 Test Connection'}
            </button>
          </div>

          {testResult && (
            <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
              {testResult.message}
            </div>
          )}
        </div>

        <div className="settings-section">
          <h2>General Settings</h2>

          <div className="form-group">
            <label htmlFor="theme">Theme</label>
            <select
              id="theme"
              value={settings.theme}
              onChange={(e) => handleChange('theme', e.target.value)}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="max-history">Max Video History</label>
            <input
              id="max-history"
              type="number"
              min="10"
              max="500"
              value={settings.max_history}
              onChange={(e) => handleChange('max_history', parseInt(e.target.value))}
            />
            <small>Maximum number of videos to keep in history</small>
          </div>

          <div className="checkbox-group">
            <input
              id="notifications"
              type="checkbox"
              checked={settings.enable_notifications}
              onChange={(e) => handleChange('enable_notifications', e.target.checked)}
            />
            <label htmlFor="notifications">Enable notifications for ingestion status</label>
          </div>

          <div className="checkbox-group">
            <input
              id="auto-ingest"
              type="checkbox"
              checked={settings.auto_ingest}
              onChange={(e) => handleChange('auto_ingest', e.target.checked)}
            />
            <label htmlFor="auto-ingest">Auto-ingest videos when detected (experimental)</label>
          </div>
        </div>

        <div className="settings-section">
          <h2>About</h2>
          <p>
            <strong>Alexandria AI</strong> v1.0.0
          </p>
          <p>
            Your intelligent learning companion - AI-powered video analysis and smart learning assistance.
          </p>
          <p>
            <a href="https://github.com/your-repo" target="_blank" rel="noopener noreferrer">
              GitHub Repository
            </a>
            {' • '}
            <a href="https://github.com/your-repo/issues" target="_blank" rel="noopener noreferrer">
              Report Issues
            </a>
          </p>
        </div>
      </div>

      <div className="options-footer">
        <button 
          className="btn btn-reset"
          onClick={handleReset}
        >
          Reset to Defaults
        </button>
        <button 
          className="btn btn-save"
          onClick={handleSave}
        >
          {saved ? '✓ Saved!' : '💾 Save Settings'}
        </button>
      </div>
    </div>
  );
}
