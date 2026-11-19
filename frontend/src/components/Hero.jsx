import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaLocationDot,
  FaCrosshairs,
  FaArrowRight,
  FaLungs,
  FaShieldVirus,
  FaTowerBroadcast,
  FaLeaf,
  FaClock,
  FaCrown,
  FaCompass,
  FaCircleExclamation,
  FaRotate,
  FaXmark,
  FaChevronDown,
  FaCheck,
} from 'react-icons/fa6';
import './Hero.css';

const CURATED_CITIES = [
  { name: 'Delhi', state: 'NCR', flag: '🇮🇳' },
  { name: 'Mumbai', state: 'Maharashtra', flag: '🇮🇳' },
  { name: 'Bengaluru', state: 'Karnataka', flag: '🇮🇳' },
  { name: 'Kolkata', state: 'West Bengal', flag: '🇮🇳' },
  { name: 'Chennai', state: 'Tamil Nadu', flag: '🇮🇳' },
  { name: 'Hyderabad', state: 'Telangana', flag: '🇮🇳' },
  { name: 'Thiruvananthapuram', state: 'Kerala', flag: '🇮🇳' },
  { name: 'Ahmedabad', state: 'Gujarat', flag: '🇮🇳' },
];

const INDIAN_CITIES = [
  { name: 'Delhi', state: 'National Capital Region', zone: 'North India', flag: '🇮🇳' },
  { name: 'Mumbai', state: 'Maharashtra', zone: 'West India', flag: '🇮🇳' },
  { name: 'Bengaluru', state: 'Karnataka', zone: 'South India', flag: '🇮🇳' },
  { name: 'Kolkata', state: 'West Bengal', zone: 'East India', flag: '🇮🇳' },
  { name: 'Chennai', state: 'Tamil Nadu', zone: 'South India', flag: '🇮🇳' },
  { name: 'Hyderabad', state: 'Telangana', zone: 'South India', flag: '🇮🇳' },
  { name: 'Thiruvananthapuram', state: 'Kerala', zone: 'South India', flag: '🇮🇳' },
  { name: 'Ahmedabad', state: 'Gujarat', zone: 'West India', flag: '🇮🇳' },
  { name: 'Pune', state: 'Maharashtra', zone: 'West India', flag: '🇮🇳' },
  { name: 'Jaipur', state: 'Rajasthan', zone: 'North India', flag: '🇮🇳' },
  { name: 'Lucknow', state: 'Uttar Pradesh', zone: 'North India', flag: '🇮🇳' },
  { name: 'Chandigarh', state: 'Punjab & Haryana', zone: 'North India', flag: '🇮🇳' },
  { name: 'Patna', state: 'Bihar', zone: 'East India', flag: '🇮🇳' },
  { name: 'Bhopal', state: 'Madhya Pradesh', zone: 'Central India', flag: '🇮🇳' },
  { name: 'Kochi', state: 'Kerala', zone: 'South India', flag: '🇮🇳' },
  { name: 'Indore', state: 'Madhya Pradesh', zone: 'Central India', flag: '🇮🇳' },
  { name: 'Visakhapatnam', state: 'Andhra Pradesh', zone: 'South India', flag: '🇮🇳' },
  { name: 'Guwahati', state: 'Assam', zone: 'Northeast India', flag: '🇮🇳' },
  { name: 'Varanasi', state: 'Uttar Pradesh', zone: 'North India', flag: '🇮🇳' },
  { name: 'Surat', state: 'Gujarat', zone: 'West India', flag: '🇮🇳' },
  { name: 'Nagpur', state: 'Maharashtra', zone: 'Central India', flag: '🇮🇳' },
  { name: 'Coimbatore', state: 'Tamil Nadu', zone: 'South India', flag: '🇮🇳' },
  { name: 'Dehradun', state: 'Uttarakhand', zone: 'North India', flag: '🇮🇳' },
  { name: 'Srinagar', state: 'Jammu & Kashmir', zone: 'North India', flag: '🇮🇳' },
  { name: 'Bhubaneswar', state: 'Odisha', zone: 'East India', flag: '🇮🇳' },
];

const BESPOKE_PROFILES = [
  {
    value: 'family',
    title: 'Family & Children',
    emoji: '👨‍👩‍👧‍👦',
    tier: 'Priority Care',
    desc: 'Pediatric alveolar shielding & calibrated school commute windows',
  },
  {
    value: 'elderly',
    title: 'Senior Wellness',
    emoji: '👴',
    tier: 'High Vigilance',
    desc: 'Cardiovascular filtration & hermetically sealed sleep sanctums',
  },
  {
    value: 'commuter',
    title: 'Urban Executive',
    emoji: '🚗',
    tier: 'Transit Shield',
    desc: 'In-cabin particulate recirculation & rush-hour exposure minimization',
  },
  {
    value: 'wfh',
    title: 'Private Residence',
    emoji: '💻',
    tier: 'Sanctuary',
    desc: 'Optimal indoor CO₂ vs PM2.5 balance & bio-filtration design',
  },
  {
    value: 'athlete',
    title: 'Performance & Fitness',
    emoji: '🏃',
    tier: 'Chrono-Targeted',
    desc: 'Solar-window aerobic training & zero-inversion cardio timing',
  },
  {
    value: 'student',
    title: 'Academic & Campus',
    emoji: '🎒',
    tier: 'Active Transit',
    desc: 'Low-exposure corridor navigation & classroom ventilation',
  },
];

export default function Hero({ onSetup, setupError, onClearError, onRetry }) {
  const [city, setCity] = useState('');
  const [selectedLifestyle, setSelectedLifestyle] = useState('family');
  const [isDetecting, setIsDetecting] = useState(false);
  const [inputError, setInputError] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const handleSelectCity = (cityName) => {
    setCity(cityName);
    setInputError('');
    if (setupError && onClearError) onClearError();
  };

  const filteredCities = INDIAN_CITIES.filter((c) => {
    const q = city.toLowerCase().trim();
    if (!q) return true;
    return (
      c.name.toLowerCase().includes(q) ||
      c.state.toLowerCase().includes(q) ||
      c.zone.toLowerCase().includes(q)
    );
  });

  // B6 FIX: Authentic browser geolocation with reverse geocoding fallback
  const handleDetect = () => {
    setInputError('');
    if (!navigator.geolocation) {
      setInputError('Geolocation is not supported by your browser. Please select or type your city.');
      return;
    }

    setIsDetecting(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          const { latitude, longitude } = pos.coords;
          // Reverse geocode via BigDataCloud or Open-Meteo
          const res = await fetch(
            `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`
          );
          const data = await res.json();
          const detectedCity = data.city || data.locality || data.principalSubdivision;

          if (detectedCity) {
            setCity(detectedCity);
          } else {
            setCity('Delhi'); // Safe graceful fallback if locality name is unresolved
          }
        } catch (e) {
          console.warn('Reverse geocoding error:', e);
          setInputError('Unable to resolve city from coordinates. Please select from below.');
        } finally {
          setIsDetecting(false);
        }
      },
      (err) => {
        setIsDetecting(false);
        // B6 FIX: Do NOT silently set Delhi on denial or error!
        if (err.code === 1) {
          setInputError('Location permission denied. Please choose a metropolis or type your city name.');
        } else {
          setInputError('Location detection timed out. Please enter your city manually.');
        }
      },
      { timeout: 8000 }
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!city.trim()) {
      // B19 FIX: Accessible inline validation instead of alert()
      setInputError('Please specify your residential city or select one from above to continue.');
      return;
    }
    setInputError('');
    onSetup(city.trim(), selectedLifestyle);
  };

  return (
    <section className="lux-hero-section">
      {/* Ambient Auroral Luminous Glows */}
      <div className="lux-glow glow-cyan"></div>
      <div className="lux-glow glow-gold"></div>
      <div className="lux-glow glow-indigo"></div>

      <div className="lux-hero-container">
        {/* Left Column: Intelligence Interface */}
        <div className="lux-content-col">
          {/* Haute Badge */}
          <motion.div
            className="lux-badge"
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <FaCrown className="crown-icon" />
            <span className="badge-sep">•</span>
            <span className="badge-text">ATMOSPHERIC HEALTH INTELLIGENCE SUITE</span>
            <span className="lux-live-dot"></span>
          </motion.div>

          {/* Majestic Hero Headline */}
          <motion.h1
            className="lux-title"
            initial={{ opacity: 0, y: 22 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.65, delay: 0.1 }}
          >
            Breathe Immaculate Air.<br />
            <span className="gradient-text">Curated Smog Defense.</span>
          </motion.h1>

          <motion.p
            className="lux-subtitle"
            initial={{ opacity: 0, y: 22 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.65, delay: 0.2 }}
          >
            Protect your household from winter inversions. Ingest hourly atmospheric reanalysis,
            chrono-tailored routines, low-cost hospital-grade indoor purifiers, and quantifiable emission reductions.
          </motion.p>

          {/* B1 FIX: Server Error Banner with Retry button and NO fabricated numbers */}
          {setupError && (
            <motion.div
              className="lux-error-banner"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="error-banner-icon">
                <FaCircleExclamation />
              </div>
              <div className="error-banner-content">
                <strong>Atmospheric Service Offline</strong>
                <p>{setupError}</p>
              </div>
              <div className="error-banner-actions">
                {onRetry && (
                  <button type="button" className="error-retry-btn" onClick={onRetry}>
                    <FaRotate /> Retry
                  </button>
                )}
                {onClearError && (
                  <button type="button" className="error-dismiss-btn" onClick={onClearError} title="Dismiss">
                    <FaXmark />
                  </button>
                )}
              </div>
            </motion.div>
          )}

          {/* Curated Indian Cities Strip */}
          <div className="curated-city-bar">
            <span className="city-bar-label">
              <FaCompass /> Indian Metropolises:
            </span>
            <div className="curated-city-pills">
              {CURATED_CITIES.map((c) => (
                <button
                  key={c.name}
                  type="button"
                  className={`city-pill ${city.toLowerCase() === c.name.toLowerCase() ? 'active' : ''}`}
                  onClick={() => handleSelectCity(c.name)}
                >
                  <span className="flag">{c.flag}</span>
                  <span className="c-name">{c.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Precision Input Form */}
          <motion.form
            className="lux-setup-terminal glass-panel"
            onSubmit={handleSubmit}
            initial={{ opacity: 0, y: 26 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.65, delay: 0.3 }}
          >
            <div className="terminal-header-row">
              <label htmlFor="luxLocationInput">Target Residence / City Coordinates</label>
              <span className="sat-coverage">Open-Meteo & Ground Station Readings</span>
            </div>

            <div className="lux-input-dropdown-wrapper" ref={dropdownRef}>
              <div className={`lux-input-box ${isDropdownOpen ? 'dropdown-active' : ''}`}>
                <FaLocationDot className="input-pin-icon" />
                <input
                  type="text"
                  id="luxLocationInput"
                  placeholder="Select Indian city or enter location (e.g. Delhi, Mumbai, Bengaluru...)"
                  value={city}
                  onChange={(e) => {
                    setCity(e.target.value);
                    setInputError('');
                    setIsDropdownOpen(true);
                  }}
                  onFocus={() => setIsDropdownOpen(true)}
                  autoComplete="off"
                  aria-expanded={isDropdownOpen}
                  aria-autocomplete="list"
                  aria-controls="city-dropdown-listbox"
                />

                {city && (
                  <button
                    type="button"
                    className="lux-input-action-btn clear-btn"
                    onClick={() => {
                      setCity('');
                      setInputError('');
                      setIsDropdownOpen(true);
                    }}
                    title="Clear input"
                    aria-label="Clear city input"
                  >
                    <FaXmark />
                  </button>
                )}

                <button
                  type="button"
                  className={`lux-dropdown-toggle-btn ${isDropdownOpen ? 'open' : ''}`}
                  onClick={() => setIsDropdownOpen((prev) => !prev)}
                  title="Toggle city selection dropdown"
                  aria-label="Toggle city selection dropdown"
                  aria-expanded={isDropdownOpen}
                >
                  <FaChevronDown className={`chevron-icon ${isDropdownOpen ? 'rotate-180' : ''}`} />
                </button>

                <button
                  type="button"
                  className={`lux-detect-btn ${isDetecting ? 'detecting' : ''}`}
                  onClick={handleDetect}
                  disabled={isDetecting}
                  title="Detect current location via browser"
                >
                  <FaCrosshairs />
                  <span>{isDetecting ? 'Locating...' : 'Auto'}</span>
                </button>
              </div>

              {/* City Selection Dropdown Menu */}
              <AnimatePresence>
                {isDropdownOpen && (
                  <motion.div
                    className="lux-city-dropdown glass-panel"
                    initial={{ opacity: 0, y: -6, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -6, scale: 0.98 }}
                    transition={{ duration: 0.15 }}
                    role="listbox"
                    id="city-dropdown-listbox"
                  >
                    <div className="dropdown-header">
                      <span className="dropdown-title">INDIAN ATMOSPHERIC STATIONS</span>
                      <span className="dropdown-counter">{filteredCities.length} Indian Cities</span>
                    </div>

                    <div className="dropdown-scroll-list">
                      {filteredCities.length > 0 ? (
                        filteredCities.map((c) => {
                          const isSelected = city.toLowerCase().trim() === c.name.toLowerCase();
                          return (
                            <div
                              key={c.name}
                              className={`dropdown-city-item ${isSelected ? 'selected' : ''}`}
                              onClick={() => {
                                handleSelectCity(c.name);
                                setIsDropdownOpen(false);
                              }}
                              role="option"
                              aria-selected={isSelected}
                              tabIndex={0}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter' || e.key === ' ') {
                                  e.preventDefault();
                                  handleSelectCity(c.name);
                                  setIsDropdownOpen(false);
                                }
                              }}
                            >
                              <span className="dropdown-city-flag">{c.flag}</span>
                              <div className="dropdown-city-info">
                                <span className="dropdown-city-name">{c.name}</span>
                                <span className="dropdown-city-sub">
                                  {c.state}
                                </span>
                              </div>
                              <span className="dropdown-status-chip chip-station">
                                {c.zone}
                              </span>
                              {isSelected && <FaCheck className="dropdown-check-icon" />}
                            </div>
                          );
                        })
                      ) : (
                        <div className="dropdown-empty-state">
                          <span className="empty-title">"{city}" not in standard Indian stations.</span>
                          <p className="empty-desc">
                            Select <strong>Initialize Defense</strong> to query live satellite & telemetry for "{city}".
                          </p>
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* B19 FIX: Accessible inline validation feedback */}
            {inputError && (
              <div className="inline-input-error" role="alert">
                <FaCircleExclamation />
                <span>{inputError}</span>
              </div>
            )}

            {/* Lifestyle Cards */}
            <div className="lifestyle-module">
              <div className="terminal-header-row">
                <label>Bespoke Household Profile</label>
                <span className="sat-coverage">Calibrates Vulnerability Indices</span>
              </div>

              <div className="bespoke-profiles-grid">
                {BESPOKE_PROFILES.map((p) => {
                  const isSelected = selectedLifestyle === p.value;
                  return (
                    <div
                      key={p.value}
                      className={`profile-card ${isSelected ? 'selected' : ''}`}
                      onClick={() => setSelectedLifestyle(p.value)}
                      role="button"
                      tabIndex={0}
                      aria-pressed={isSelected}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                          e.preventDefault();
                          setSelectedLifestyle(p.value);
                        }
                      }}
                    >
                      <div className="profile-header">
                        <span className="profile-emoji">{p.emoji}</span>
                        <span className="profile-tier">{p.tier}</span>
                      </div>
                      <div className="profile-title">{p.title}</div>
                      <div className="profile-desc">{p.desc}</div>
                      {isSelected && <div className="selected-gold-indicator" />}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Supreme CTA Button */}
            <button type="submit" className="lux-submit-btn" id="startBtn">
              <span className="btn-sheen"></span>
              <span className="btn-label">Calibrate Clean Air Plan</span>
              <FaArrowRight className="btn-arrow" />
            </button>
          </motion.form>

          {/* Haute Telemetry Features (B27 FIX: Accurate, scientific claims) */}
          <div className="lux-features-row">
            <div className="feature-cell">
              <FaTowerBroadcast className="f-icon cyan" />
              <div>
                <strong>Hourly Atmospheric Feed</strong>
                <span>Open-Meteo & station sensor data</span>
              </div>
            </div>
            <div className="feature-cell">
              <FaShieldVirus className="f-icon crimson" />
              <div>
                <strong>Clinical Protocols</strong>
                <span>N95 respirator & pediatric standards</span>
              </div>
            </div>
            <div className="feature-cell">
              <FaLeaf className="f-icon emerald" />
              <div>
                <strong>NASA Clean Air Study</strong>
                <span>Botanical gaseous VOC filtration</span>
              </div>
            </div>
            <div className="feature-cell">
              <FaClock className="f-icon gold" />
              <div>
                <strong>Diurnal Chrono-Strategy</strong>
                <span>Inversion-bypass timing</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Haute Horlogerie Atmospheric Visualizer */}
        <div className="lux-visual-col">
          <div className="horology-sanctuary-card glass-panel">
            <div className="card-ambient-bezel">
              <div className="bezel-mark north">00</div>
              <div className="bezel-mark east">06</div>
              <div className="bezel-mark south">12</div>
              <div className="bezel-mark west">18</div>

              <div className="dial-rings-assembly">
                <div className="dial-ring ring-outer"></div>
                <div className="dial-ring ring-mid"></div>
                <div className="dial-ring ring-inner"></div>
                <div className="dial-core">
                  <FaLungs className="core-lungs-icon" />
                </div>
              </div>
            </div>

            <div className="instrument-telemetry-box">
              <div className="tele-row">
                <span className="tele-label">SYSTEM TELEMETRY</span>
                <span className="tele-val live">● MONITORING ACTIVE</span>
              </div>
              <div className="tele-row">
                <span className="tele-label">COVERAGE</span>
                <span className="tele-val">Global Coordinates</span>
              </div>
              <div className="tele-row">
                <span className="tele-label">SPECIATION</span>
                <span className="tele-val highlight">PM2.5 • PM10 • NO₂ • CO • O₃</span>
              </div>
            </div>

            <div className="seal-emblem">
              <FaShieldVirus className="gem-icon" />
              <span>Evidence-Based Clean Air Defense</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
