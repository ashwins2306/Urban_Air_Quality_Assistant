import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaCalendarCheck,
  FaLightbulb,
  FaSeedling,
  FaArrowsRotate,
  FaClock,
  FaArrowRight,
  FaCheck,
  FaTriangleExclamation,
} from 'react-icons/fa6';
import { fetchRoutines } from '../utils/api';
import './DailyRoutines.css';

const LIFESTYLE_TABS = [
  { id: 'family', label: '👨‍👩‍👧‍👦 Family with Kids' },
  { id: 'elderly', label: '👴 Elderly at Home' },
  { id: 'commuter', label: '🚗 Daily Commuter' },
  { id: 'student', label: '🎒 Student' },
  { id: 'wfh', label: '💻 Work from Home' },
  { id: 'athlete', label: '🏃 Fitness Enthusiast' },
  { id: 'outdoor-worker', label: '👷 Outdoor Worker' },
];

export default function DailyRoutines({ city, lifestyle: initialLifestyle, aqiData }) {
  const [activeLifestyle, setActiveLifestyle] = useState(initialLifestyle || 'family');
  const [routines, setRoutines] = useState([]);
  const [insight, setInsight] = useState('');
  const [savings, setSavings] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // B10 FIX: Request sequence counter to cancel in-flight stale responses
  const reqSequenceRef = useRef(0);

  const loadRoutinesForTab = (targetLifestyle) => {
    const currentSeq = ++reqSequenceRef.current;
    setLoading(true);
    setError(null);
    setRoutines([]); // B10 FIX: Clear stale routines immediately so previous timeline doesn't linger

    const aqiNumber = aqiData?.aqi ?? 150; // B7 FIX: nullish coalescing

    fetchRoutines(city, targetLifestyle, aqiNumber)
      .then((res) => {
        // Only apply if this response corresponds to the latest requested tab
        if (currentSeq === reqSequenceRef.current) {
          setRoutines(res.data.routines || []);
          setInsight(res.data.insight || '');
          setSavings(res.data.savings || '');
          setLoading(false);
        }
      })
      .catch((err) => {
        if (currentSeq === reqSequenceRef.current) {
          console.error('Failed to fetch routines', err);
          setError('Failed to load routine schedule for this profile. Please try again.');
          setRoutines([]);
          setLoading(false);
        }
      });
  };

  useEffect(() => {
    loadRoutinesForTab(activeLifestyle);
  }, [city, activeLifestyle, aqiData?.aqi]);

  // B13 FIX: Calculate emission optimization score dynamically from routine items
  const lowEmissionCount = routines.filter((r) => r.emission_level === 'low').length;
  const targetPct = routines.length > 0 ? Math.round((lowEmissionCount / routines.length) * 100) : 70;

  const smartSwaps = [
    {
      from: 'Solo drive in rush-hour traffic',
      to: 'Carpool or electric metro + N95',
      reduction: '4.2 kg CO₂',
      benefit: 'Reduces direct exhaust particulate inhalation by 65%',
    },
    {
      from: 'Morning jog at 7:00 AM',
      to: 'Indoor aerobic session / yoga',
      reduction: '0 kg CO₂',
      benefit: 'Prevents 10x deep PM2.5 lung deposition during winter inversion',
    },
    {
      from: 'Open windows at breakfast',
      to: 'Seal windows; run HEPA on high',
      reduction: 'Zero particulate surge',
      benefit: 'Blocks 80% of outdoor particulate spike from morning road gridlock',
    },
    {
      from: 'High-heat open gas burner',
      to: 'Induction cooktop with range hood',
      reduction: '1.2 kg CO₂',
      benefit: 'Eliminates indoor NO₂ and ultra-fine carbon spikes',
    },
  ];

  return (
    <div className="section" id="routines">
      {/* Header */}
      <div className="section-header">
        <div className="header-badge-row">
          <span className="chrono-badge">
            <FaClock /> Chrono-Atmospheric Scheduler
          </span>
          <span className="target-city-badge">
            {city || 'Target City'} • AQI {aqiData?.aqi ?? 150}
          </span>
        </div>
        <h2>
          <FaCalendarCheck /> Low-Emission Daily Routines
        </h2>
        <p className="section-desc">
          Atmospheric smog follows a sharp diurnal rhythm: thermal inversion traps toxins near ground level at dawn and dusk.
          These AI-optimized schedules shift your high-exertion and transit windows to minimize personal inhalation and household emissions.
        </p>
      </div>

      {/* Interactive Lifestyle Switcher Tabs */}
      <div className="lifestyle-tabs-wrapper">
        <div className="lifestyle-tabs-label">Switch Lifestyle Profile:</div>
        <div className="lifestyle-tabs-strip">
          {LIFESTYLE_TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`lifestyle-tab-btn ${activeLifestyle === tab.id ? 'active' : ''}`}
              onClick={() => {
                setActiveLifestyle(tab.id);
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="routine-layout-container">
        {/* Left Column: Timeline */}
        <div className="routine-timeline-column">
          {loading ? (
            <div className="routine-loading-state">
              <div className="loader-ring"></div>
              <span>Synthesizing chronological clean-air schedule for {activeLifestyle}...</span>
            </div>
          ) : error ? (
            // B10 FIX: Clear error state with retry button instead of showing stale data
            <div className="routine-error-card">
              <FaTriangleExclamation className="err-icon" />
              <div>
                <strong>Schedule Unavailable</strong>
                <p>{error}</p>
              </div>
              <button
                type="button"
                className="routine-retry-btn"
                onClick={() => loadRoutinesForTab(activeLifestyle)}
              >
                <FaArrowsRotate /> Retry
              </button>
            </div>
          ) : routines.length === 0 ? (
            <div className="routine-empty-card">
              <p>No routine schedule generated for this profile yet.</p>
            </div>
          ) : (
            <div className="routine-timeline-feed">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeLifestyle}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ duration: 0.35 }}
                >
                  {routines.map((item, idx) => (
                    <div key={idx} className="timeline-card-wrapper">
                      {/* Timeline Marker */}
                      <div className="timeline-marker">
                        <div className={`marker-dot ${item.emission_level}`} />
                        <div className="marker-line" />
                      </div>

                      {/* Card Content */}
                      <div className="timeline-content-card glass-panel">
                        <div className="timeline-top-bar">
                          <span className="time-display-pill">
                            <FaClock /> {item.time}
                          </span>
                          <span className={`emission-rating-chip ${item.emission_level}`}>
                            {item.emission_level} emission
                          </span>
                        </div>

                        <h4 className="timeline-item-title">{item.title}</h4>
                        <p className="timeline-item-desc">{item.description}</p>

                        {item.tags && item.tags.length > 0 && (
                          <div className="timeline-tag-list">
                            {item.tags.map((tag, tIdx) => (
                              <span key={tIdx} className="timeline-pill-tag">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </motion.div>
              </AnimatePresence>
            </div>
          )}
        </div>

        {/* Right Column: Insights & Swaps */}
        <div className="routine-sidebar-column">
          {/* Key Atmospheric Insight */}
          <div className="insight-hero-card glass-panel">
            <div className="insight-top">
              <div className="insight-icon-box">
                <FaLightbulb />
              </div>
              <div>
                <h4>Smog Chrono-Strategy</h4>
                <span className="insight-sub">Scientific Timing Principle</span>
              </div>
            </div>
            <p className="insight-text">
              {insight ||
                'Winter smog in urban basins is trapped under a cold nocturnal air lid (temperature inversion). Peak particle density occurs from 05:00 to 09:30 AM and 18:30 to 22:00 PM. Keep your family indoors and run HEPA air scrubbers during these windows.'}
            </p>
          </div>

          {/* Emission Savings Meter (B13 FIX: Dynamic Target Calculation) */}
          <div className="savings-meter-card glass-panel">
            <div className="savings-header">
              <FaSeedling className="savings-icon" />
              <div>
                <h4>Household Emission Impact</h4>
                <span className="savings-sub">Calculated for this profile</span>
              </div>
            </div>

            <div className="savings-visual-row">
              <div className="savings-bar-container">
                <div className="savings-bar-fill" style={{ width: `${targetPct}%` }}></div>
              </div>
              <span className="savings-pct">{targetPct}% Optimized</span>
            </div>

            <p className="savings-desc">
              {savings ||
                'Following this schedule cuts daily particulate exposure by 55% and reduces household travel emissions by 3.4 kg CO₂ per day.'}
            </p>
          </div>

          {/* Smart Swaps Deck */}
          <div className="smart-swaps-deck glass-panel">
            <div className="swaps-header">
              <FaArrowsRotate className="swaps-icon" />
              <div>
                <h4>High-Impact Smart Swaps</h4>
                <span className="swaps-sub">Adopt cleaner alternatives</span>
              </div>
            </div>

            <div className="swaps-list">
              {smartSwaps.map((swap, sIdx) => (
                <div key={sIdx} className="swap-deck-card">
                  <div className="swap-before-after">
                    <div className="swap-box from">
                      <span className="side-tag">REPLACE</span>
                      <div className="action-txt">{swap.from}</div>
                    </div>
                    <div className="swap-connector">
                      <FaArrowRight />
                    </div>
                    <div className="swap-box to">
                      <span className="side-tag">ADOPT</span>
                      <div className="action-txt">{swap.to}</div>
                    </div>
                  </div>

                  <div className="swap-benefit-footer">
                    <FaCheck className="benefit-check" />
                    <span>{swap.benefit}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
