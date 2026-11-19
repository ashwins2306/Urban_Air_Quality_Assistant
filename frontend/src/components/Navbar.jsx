import React from 'react';
import {
  FaWind,
  FaChartLine,
  FaClockRotateLeft,
  FaCalendarCheck,
  FaHouseChimney,
  FaLeaf,
  FaChartPie,
  FaRobot,
  FaLocationDot,
  FaRotate,
} from 'react-icons/fa6';
import './Navbar.css';

export default function Navbar({
  currentSection,
  onNavigate,
  onToggleChat,
  city,
  onChangeCity,
}) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: FaChartLine },
    { id: 'chrono', label: 'Chrono-Intelligence', icon: FaClockRotateLeft },
    { id: 'routines', label: 'Daily Routines', icon: FaCalendarCheck },
    { id: 'indoor', label: 'Indoor Hacks', icon: FaHouseChimney },
    { id: 'alternatives', label: 'Alternatives', icon: FaLeaf },
    { id: 'impact', label: 'Impact', icon: FaChartPie },
  ];

  return (
    <>
      <nav className="main-nav">
        <div className="nav-left">
          <div
            className="nav-brand"
            onClick={() => onNavigate('dashboard')}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onNavigate('dashboard');
              }
            }}
            role="button"
            tabIndex={0}
            aria-label="BreatheEasy Home Dashboard"
          >
            <div className="brand-icon">
              <FaWind />
            </div>
            <div className="brand-text-col">
              <span className="brand-name">BreatheEasy</span>
              <span className="brand-tagline">Clean Air Companion</span>
            </div>
          </div>

          {city && (
            <div className="nav-location-pill" title="Current Monitored Location">
              <FaLocationDot className="pin-icon" />
              <span className="nav-city-name">{city}</span>
              {onChangeCity && (
                <button
                  type="button"
                  className="change-city-btn"
                  onClick={onChangeCity}
                  title="Switch Location"
                >
                  <FaRotate /> Change
                </button>
              )}
            </div>
          )}
        </div>

        <div className="nav-links">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                className={`nav-link ${currentSection === item.id ? 'active' : ''}`}
                onClick={() => onNavigate(item.id)}
              >
                <Icon className="nav-icon" />
                <span>{item.label}</span>
                {currentSection === item.id && <span className="active-glow-bar" />}
              </button>
            );
          })}
        </div>

        <div className="nav-right">
          <button
            type="button"
            className="ai-chat-toggle"
            onClick={onToggleChat}
            title="Open AI Smog Advisor"
          >
            <FaRobot />
            <span className="ai-chat-label">Ask AI</span>
            <span className="pulse-dot"></span>
          </button>
        </div>
      </nav>

      {/* Mobile navigation bottom bar */}
      <nav className="mobile-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              type="button"
              className={`mobile-nav-link ${currentSection === item.id ? 'active' : ''}`}
              onClick={() => onNavigate(item.id)}
            >
              <Icon />
              <span>{item.label.split(' ')[0]}</span>
            </button>
          );
        })}
      </nav>
    </>
  );
}
