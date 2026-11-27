import React, { useState, useRef, useEffect } from 'react';
import {
  FaRobot,
  FaXmark,
  FaPaperPlane,
  FaCircleInfo,
  FaKey,
  FaUser,
  FaLocationDot,
  FaShieldHeart,
  FaCircleExclamation,
} from 'react-icons/fa6';
import { sendChatMessage } from '../utils/api';
import './AIChatPanel.css';

// B16 FIX: Markdown parser for bold text, bullet points, numbered lists, and headers
function renderFormattedContent(text) {
  if (!text) return null;
  const lines = text.split('\n');

  return lines.map((line, lIdx) => {
    const trimmed = line.trim();

    // Check header
    if (trimmed.startsWith('### ')) {
      return (
        <h5 key={lIdx} className="chat-markdown-h5">
          {renderInlineBold(trimmed.substring(4))}
        </h5>
      );
    }

    // Check bullet points
    if (trimmed.startsWith('• ') || trimmed.startsWith('* ') || trimmed.startsWith('- ')) {
      const bulletContent = trimmed.substring(2);
      return (
        <li key={lIdx} className="chat-markdown-li">
          {renderInlineBold(bulletContent)}
        </li>
      );
    }

    // Check numbered list
    const numMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
    if (numMatch) {
      return (
        <li key={lIdx} className="chat-markdown-num-li">
          <span className="num-prefix">{numMatch[1]}.</span>
          <span>{renderInlineBold(numMatch[2])}</span>
        </li>
      );
    }

    // Paragraph
    return (
      <p key={lIdx} className="chat-markdown-p">
        {renderInlineBold(line)}
      </p>
    );
  });
}

function renderInlineBold(str) {
  const parts = [];
  const regex = /\*\*(.*?)\*\*/g;
  let lastIndex = 0;
  let match;
  let pIdx = 0;

  while ((match = regex.exec(str)) !== null) {
    if (match.index > lastIndex) {
      parts.push(str.substring(lastIndex, match.index));
    }
    parts.push(
      <strong key={pIdx++} className="chat-bold-token">
        {match[1]}
      </strong>
    );
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < str.length) {
    parts.push(str.substring(lastIndex));
  }

  return parts.length > 0 ? parts : str;
}

export default function AIChatPanel({ isOpen, onClose, city, lifestyle, aqiData }) {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content:
        'Hello! 👋 I am your BreatheEasy AI clean air advisor.\n\nI can help your household with:\n• 🌍 Real-time interpretation of local particulate levels\n• 🏠 Room-by-room indoor filtration and air sealing hacks\n• 🚲 Low-exposure commute schedules & sports timing\n• 👨‍👩‍👧 Pediatric & elderly respiratory vulnerability guidance\n• 📊 Practical household carbon & smog reduction swaps\n\nWhat air quality challenge can I help you resolve right now?',
    },
  ]);

  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('gemini_api_key') || '');
  const [keyInput, setKeyInput] = useState('');
  // B2 FIX: Track whether server actually confirms a Gemini connection vs offline rule engine
  const [lastEngineSource, setLastEngineSource] = useState('clinical_engine');

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const suggestions = [
    { text: 'Best mask for kids?', q: 'What is the most effective and safe mask for children during severe winter smog?' },
    { text: 'Reduce cooking NO2', q: 'How can I prevent cooking fumes and NO2 spikes inside our home during winter?' },
    { text: 'Safest outdoor hours?', q: 'What are the safest hours of the day to step outside or ventilate rooms?' },
    { text: 'Build DIY HEPA box', q: 'How do I assemble a DIY Corsi-Rosenthal box air purifier at home under $30?' },
  ];

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || isTyping) return;

    const userMsg = { role: 'user', content: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    if (!queryText) setInput('');
    setIsTyping(true);

    try {
      const context = {
        city: city || 'Urban Area',
        lifestyle: lifestyle || 'family',
        aqi: aqiData?.aqi ?? 150, // B7 FIX
      };

      // B17 FIX: Pass conversation history turns for conversational context memory
      const history = messages
        .filter((m) => m.role === 'user' || m.role === 'bot')
        .slice(-6)
        .map((m) => ({
          role: m.role === 'user' ? 'user' : 'model',
          content: m.content,
        }));

      // B2 FIX: Send the apiKey in the POST request body over HTTPS
      const res = await sendChatMessage(textToSend, context, apiKey || null, history);

      if (res.data && res.data.response) {
        setLastEngineSource(res.data.source || 'clinical_engine');
        setMessages((prev) => [
          ...prev,
          { role: 'bot', content: res.data.response, source: res.data.source },
        ]);
      } else {
        throw new Error('Empty response received from chat API');
      }
    } catch (err) {
      console.error('Chat error:', err);
      // B3 FIX: Do NOT disguise chat network/server failure as a happy AI answer!
      setMessages((prev) => [
        ...prev,
        {
          role: 'error',
          content:
            '⚠️ Connection Error: Unable to reach the assistant server. Please verify that your backend server is running and try again.',
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const saveApiKey = () => {
    if (keyInput.trim()) {
      localStorage.setItem('gemini_api_key', keyInput.trim());
      setApiKey(keyInput.trim());
    }
    setShowApiKeyModal(false);
  };

  const clearApiKey = () => {
    localStorage.removeItem('gemini_api_key');
    setApiKey('');
    setLastEngineSource('clinical_engine');
  };

  return (
    <>
      {/* B19 FIX: aria-hidden when closed so elements are removed from accessibility tree */}
      <div
        className={`ai-chat-panel ${isOpen ? 'open' : ''}`}
        aria-hidden={!isOpen}
      >
        {/* Header */}
        <div className="chat-header">
          <div className="chat-header-info">
            <div className="chat-avatar">
              <FaRobot />
            </div>
            <div>
              <div className="chat-title-row">
                <h4>BreatheEasy AI</h4>
                <span className="live-ai-chip">Active</span>
              </div>
              {/* B2 FIX: Honest status reporting; only says Gemini connected if server confirms it */}
              <span className="chat-status">
                {lastEngineSource === 'gemini'
                  ? '⚡ Gemini 2.0 Flash Connected'
                  : apiKey
                  ? '🔑 Custom Key Saved (Offline Engine Active)'
                  : '🤖 Clinical Clean-Air Rule Engine'}
              </span>
            </div>
          </div>
          <button
            type="button"
            className="chat-close"
            onClick={onClose}
            title="Close Chat"
            tabIndex={isOpen ? 0 : -1}
          >
            <FaXmark />
          </button>
        </div>

        {/* Telemetry Context Strip */}
        <div className="chat-telemetry-banner">
          <div className="telemetry-pill">
            <FaLocationDot className="t-icon" />
            <span>{aqiData?.city || city || 'Current City'}</span>
          </div>
          <div className="telemetry-pill">
            <span
              className="aqi-dot-small"
              style={{ background: aqiData?.color || '#ef4444' }}
            />
            <span>AQI {aqiData?.aqi ?? 150}</span>
          </div>
          <div className="telemetry-pill">
            <FaShieldHeart className="t-icon" />
            <span>{lifestyle || 'family'}</span>
          </div>
        </div>

        {/* Message Stream */}
        <div className="chat-messages">
          {messages.map((msg, idx) => {
            const isError = msg.role === 'error';
            return (
              <div
                key={idx}
                className={`chat-message ${msg.role} ${isError ? 'error-bubble' : ''}`}
              >
                <div className="message-avatar">
                  {isError ? (
                    <FaCircleExclamation style={{ color: '#f87171' }} />
                  ) : msg.role === 'bot' ? (
                    <FaRobot />
                  ) : (
                    <FaUser />
                  )}
                </div>
                <div className="message-content">
                  {/* B16 FIX: Formatted markdown lines */}
                  {renderFormattedContent(msg.content)}
                </div>
              </div>
            );
          })}

          {isTyping && (
            <div className="chat-message bot">
              <div className="message-avatar">
                <FaRobot />
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Chips */}
        <div className="chat-suggestions">
          {suggestions.map((s, idx) => (
            <button
              key={idx}
              type="button"
              className="suggestion-chip"
              onClick={() => handleSend(s.q)}
              tabIndex={isOpen ? 0 : -1}
            >
              {s.text}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="chat-input-area">
          <div className="api-key-notice">
            <FaCircleInfo />
            <span>
              {apiKey ? (
                <>
                  Custom Gemini Key configured.{' '}
                  <button
                    type="button"
                    className="link-btn"
                    onClick={clearApiKey}
                    tabIndex={isOpen ? 0 : -1}
                  >
                    Clear key
                  </button>
                </>
              ) : (
                <>
                  Built-in clinical engine active.{' '}
                  <button
                    type="button"
                    className="link-btn"
                    onClick={() => setShowApiKeyModal(true)}
                    tabIndex={isOpen ? 0 : -1}
                  >
                    Add Gemini API key
                  </button>{' '}
                  for live LLM streaming.
                </>
              )}
            </span>
          </div>

          <div className="chat-input-row">
            <input
              type="text"
              placeholder="Ask about N95 masks, DIY purifiers, kid safety..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              tabIndex={isOpen ? 0 : -1}
            />
            <button
              type="button"
              className="chat-send"
              onClick={() => handleSend()}
              disabled={isTyping}
              title="Send Message"
              tabIndex={isOpen ? 0 : -1}
            >
              <FaPaperPlane />
            </button>
          </div>
        </div>
      </div>

      {/* API Key Modal */}
      {showApiKeyModal && (
        <div className="modal-overlay" onClick={() => setShowApiKeyModal(false)}>
          <div className="modal-card glass-panel" onClick={(e) => e.stopPropagation()}>
            <h3>
              <FaKey /> Connect Gemini API Key
            </h3>
            <p>
              Enhance BreatheEasy with live Gemini 2.0 Flash reasoning for customized family health advisories.{' '}
              <a
                href="https://aistudio.google.com/apikey"
                target="_blank"
                rel="noreferrer"
              >
                Get a free key from Google AI Studio →
              </a>
            </p>
            <input
              type="password"
              placeholder="AIzaSy..."
              value={keyInput}
              onChange={(e) => setKeyInput(e.target.value)}
              autoFocus
            />
            <div className="modal-actions">
              <button
                type="button"
                className="btn-secondary"
                onClick={() => setShowApiKeyModal(false)}
              >
                Cancel
              </button>
              <button type="button" className="cta-button" onClick={saveApiKey}>
                Save Key
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
