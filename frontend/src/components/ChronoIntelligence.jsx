import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaClockRotateLeft,
  FaVolumeHigh,
  FaVolumeXmark,
  FaPlay,
  FaPause,
  FaCalendarPlus,
  FaFileArrowDown,
  FaSun,
  FaMoon,
  FaCloudSun,
  FaWind,
  FaShieldVirus,
  FaTriangleExclamation,
  FaCheck,
  FaRotate,
  FaRobot,
  FaArrowUpRightFromSquare,
  FaUsers,
  FaPersonWalking,
  FaLaptopCode,
  FaBriefcase,
  FaPersonCane,
  FaGraduationCap,
} from 'react-icons/fa6';
import { fetchChronoIntelligence } from '../utils/api';
import './ChronoIntelligence.css';

const LIFESTYLE_OPTIONS = [
  { value: 'family', label: 'Family & Children', icon: FaUsers },
  { value: 'elderly', label: 'Senior Wellness', icon: FaPersonCane },
  { value: 'commuter', label: 'Urban Executive', icon: FaBriefcase },
  { value: 'wfh', label: 'Home Office / WFH', icon: FaLaptopCode },
  { value: 'athlete', label: 'Performance Athlete', icon: FaPersonWalking },
  { value: 'student', label: 'Academic Student', icon: FaGraduationCap },
];

export default function ChronoIntelligence({ city, lifestyle, aqiData }) {
  const [activeLifestyle, setActiveLifestyle] = useState(lifestyle || 'family');
  const [chronoData, setChronoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [speechRate, setSpeechRate] = useState(1.0);
  const [copiedCalendar, setCopiedCalendar] = useState(false);

  const utteranceRef = useRef(null);

  const loadChronoData = async (selectedLifestyle = activeLifestyle) => {
    setLoading(true);
    setError(null);
    try {
      const aqiVal = aqiData?.aqi ?? 150;
      const res = await fetchChronoIntelligence(city || 'Delhi', selectedLifestyle, aqiVal);
      setChronoData(res.data);
    } catch (err) {
      console.error('Failed to load chrono intelligence', err);
      setError('Unable to synthesize atmospheric chrono-intelligence. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChronoData(activeLifestyle);
    return () => {
      if (typeof window !== 'undefined' && window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, [city, activeLifestyle]);

  // Audio Spoken Briefing Handler
  const handleToggleAudio = () => {
    if (typeof window === 'undefined' || !window.speechSynthesis) {
      alert('Speech synthesis is not supported on this browser.');
      return;
    }

    if (isPlayingAudio) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
      return;
    }

    if (!chronoData?.spoken_briefing) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(chronoData.spoken_briefing);
    utterance.rate = speechRate;
    utterance.pitch = 1.0;

    // Choose preferred voice if available
    const voices = window.speechSynthesis.getVoices();
    const englishVoice = voices.find(
      (v) => (v.name.includes('Natural') || v.name.includes('Google') || v.lang.startsWith('en'))
    );
    if (englishVoice) {
      utterance.voice = englishVoice;
    }

    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);

    utteranceRef.current = utterance;
    setIsPlayingAudio(true);
    window.speechSynthesis.speak(utterance);
  };

  // Generate & Download .ICS Calendar File
  const handleDownloadICS = () => {
    if (!chronoData) return;

    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    const y = now.getFullYear();
    const m = pad(now.getMonth() + 1);
    const d = pad(now.getDate());

    const formatDt = (timeStr) => {
      const [hh, mm] = (timeStr || '12:00').split(':');
      return `${y}${m}${d}T${pad(hh)}${pad(mm)}00`;
    };

    let icsContent = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//BreatheEasy//ChronoIntelligence//EN',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH',
    ];

    const events = chronoData.calendar_events || [];
    events.forEach((ev, idx) => {
      const dtStart = formatDt(ev.start_time_iso);
      const dtEnd = formatDt(ev.end_time_iso);
      icsContent.push(
        'BEGIN:VEVENT',
        `UID:breatheasy-${idx}-${Date.now()}@breatheasy.cleanair`,
        `DTSTAMP:${y}${m}${d}T000000Z`,
        `DTSTART:${dtStart}`,
        `DTEND:${dtEnd}`,
        `SUMMARY:${ev.title}`,
        `DESCRIPTION:${ev.description.replace(/\n/g, ' ')}`,
        'STATUS:CONFIRMED',
        'END:VEVENT'
      );
    });

    icsContent.push('END:VCALENDAR');

    const blob = new Blob([icsContent.join('\r\n')], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `breatheasy-${city.toLowerCase()}-chrono-windows.ics`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setCopiedCalendar(true);
    setTimeout(() => setCopiedCalendar(false), 3000);
  };

  // 1-Click Google Calendar Event Link
  const getGoogleCalendarURL = () => {
    if (!chronoData || !chronoData.calendar_events || chronoData.calendar_events.length === 0) return '#';
    const ev = chronoData.calendar_events[0];
    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    const y = now.getFullYear();
    const m = pad(now.getMonth() + 1);
    const d = pad(now.getDate());

    const start = `${y}${m}${d}T${(ev.start_time_iso || '13:30').replace(':', '')}00`;
    const end = `${y}${m}${d}T${(ev.end_time_iso || '15:30').replace(':', '')}00`;

    const title = encodeURIComponent(ev.title);
    const details = encodeURIComponent(`${ev.description}\n\nGenerated by BreatheEasy Chrono-Intelligence for ${city}.`);
    const loc = encodeURIComponent(`${city}, India`);

    return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${start}/${end}&details=${details}&location=${loc}`;
  };

  return (
    <div className="section" id="chrono-intelligence">
      {/* Header Container */}
      <div className="chrono-header-container">
        <div>
          <div className="chrono-badge-row">
            <span className="chrono-ai-badge">
              <FaRobot className="robot-icon" />
              <span>GENAI CHRONO-METEOROLOGICAL SYNTHESIS</span>
            </span>
            <span className="chrono-station-chip">
              {city} • AQI {aqiData?.aqi ?? 150}
            </span>
          </div>

          <h2 className="chrono-main-title">
            <FaClockRotateLeft className="title-clock-icon" />
            <span>Hyper-Personalized Chrono-Intelligence</span>
          </h2>
          <p className="chrono-subtitle">
            Synchronize your day with boundary-layer thermal inversion cycles. Ingest diurnal particulate dispersion
            windows, audio spoken advisories, and agentic 1-click calendar sync.
          </p>
        </div>

        <button
          type="button"
          className={`chrono-refresh-btn ${loading ? 'loading' : ''}`}
          onClick={() => loadChronoData(activeLifestyle)}
          disabled={loading}
          title="Re-synthesize atmospheric intelligence"
        >
          <FaRotate className={loading ? 'spin' : ''} />
          <span>{loading ? 'Synthesizing...' : 'Re-Synthesize'}</span>
        </button>
      </div>

      {/* Household Persona Switcher */}
      <div className="chrono-persona-bar">
        <span className="persona-bar-label">
          <FaUsers /> Bespoke Household Calibration:
        </span>
        <div className="persona-pills-row">
          {LIFESTYLE_OPTIONS.map((item) => {
            const Icon = item.icon;
            const isActive = activeLifestyle === item.value;
            return (
              <button
                key={item.value}
                type="button"
                className={`chrono-persona-pill ${isActive ? 'active' : ''}`}
                onClick={() => {
                  if (activeLifestyle !== item.value) {
                    setActiveLifestyle(item.value);
                  }
                }}
              >
                <Icon className="persona-pill-icon" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <div className="chrono-loading-card glass-panel">
          <div className="chrono-loading-spinner"></div>
          <h4>Synthesizing Boundary-Layer Inversion Schedule...</h4>
          <p>Analyzing solar convection parameters, tropospheric boundary depth, and {city} hourly telemetry.</p>
        </div>
      ) : error ? (
        <div className="chrono-error-card glass-panel">
          <FaTriangleExclamation className="error-icon" />
          <p>{error}</p>
          <button type="button" className="retry-btn" onClick={() => loadChronoData(activeLifestyle)}>
            Retry Synthesis
          </button>
        </div>
      ) : chronoData ? (
        <div className="chrono-body-grid">
          {/* ================= AUDIO BRIEFING & HEADLINE HERO ================= */}
          <motion.div
            className="chrono-hero-card glass-panel"
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className="hero-top-row">
              <div className="headline-meta">
                <span className="executive-tag">EXECUTIVE ATMOSPHERIC BRIEFING</span>
                <h3 className="briefing-headline">{chronoData.briefing_headline}</h3>
              </div>

              {/* Audio Playback Controls */}
              <div className="audio-player-cluster">
                <button
                  type="button"
                  className={`audio-play-toggle-btn ${isPlayingAudio ? 'playing' : ''}`}
                  onClick={handleToggleAudio}
                  title={isPlayingAudio ? 'Pause spoken briefing' : 'Play audio spoken briefing'}
                >
                  {isPlayingAudio ? <FaPause /> : <FaPlay />}
                  <span>{isPlayingAudio ? 'Pause Briefing' : 'Play Audio Briefing'}</span>
                </button>

                {isPlayingAudio && (
                  <div className="soundwave-indicator" aria-label="Audio active">
                    <span className="wave-bar bar-1"></span>
                    <span className="wave-bar bar-2"></span>
                    <span className="wave-bar bar-3"></span>
                    <span className="wave-bar bar-4"></span>
                    <span className="wave-bar bar-5"></span>
                  </div>
                )}
              </div>
            </div>

            {/* Spoken Text Transcript */}
            <div className="briefing-transcript-box">
              <p className="transcript-text">
                <span className="quote-mark">“</span>
                {chronoData.spoken_briefing}
                <span className="quote-mark">”</span>
              </p>
              <div className="transcript-footer">
                <span className="ai-model-tag">
                  <FaRobot /> {chronoData.is_ai_generated ? 'Gemini 2.0 Flash Inversion Model' : 'Clinical Diurnal Inversion Engine'}
                </span>
                <span className="voice-speed-pill">
                  Spoken pacing: {speechRate}x
                </span>
              </div>
            </div>
          </motion.div>

          {/* ================= DIURNAL INVERSION HORIZON CARDS ================= */}
          <div className="inversion-horizon-grid">
            {/* Card 1: Hazard Peak */}
            <motion.div
              className="inversion-stage-card card-hazard glass-panel"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 }}
            >
              <div className="stage-header">
                <span className="stage-badge badge-hazard">
                  <FaTriangleExclamation /> HAZARD INVERSION PEAK
                </span>
                <span className="stage-time">{chronoData.inversion_windows.hazard_peak.time}</span>
              </div>
              <h4 className="stage-title">{chronoData.inversion_windows.hazard_peak.title}</h4>
              <p className="stage-desc">{chronoData.inversion_windows.hazard_peak.desc}</p>
              <div className="stage-footer">
                <span className="rule-chip chip-red">Zero Unmasked Outdoor Exposure</span>
              </div>
            </motion.div>

            {/* Card 2: Solar Dispersion Window */}
            <motion.div
              className="inversion-stage-card card-optimal glass-panel"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.15 }}
            >
              <div className="stage-header">
                <span className="stage-badge badge-optimal">
                  <FaSun /> SOLAR DISPERSION WINDOW
                </span>
                <span className="stage-time">{chronoData.inversion_windows.optimal_window.time}</span>
              </div>
              <h4 className="stage-title">{chronoData.inversion_windows.optimal_window.title}</h4>
              <p className="stage-desc">{chronoData.inversion_windows.optimal_window.desc}</p>
              <div className="stage-footer">
                <span className="rule-chip chip-cyan">Safe Cross-Ventilation & Transit</span>
              </div>
            </motion.div>

            {/* Card 3: Nocturnal Boundary Inversion */}
            <motion.div
              className="inversion-stage-card card-sanctuary glass-panel"
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 }}
            >
              <div className="stage-header">
                <span className="stage-badge badge-sanctuary">
                  <FaMoon /> NOCTURNAL BOUNDARY INVERSION
                </span>
                <span className="stage-time">{chronoData.inversion_windows.sanctuary_sealing.time}</span>
              </div>
              <h4 className="stage-title">{chronoData.inversion_windows.sanctuary_sealing.title}</h4>
              <p className="stage-desc">{chronoData.inversion_windows.sanctuary_sealing.desc}</p>
              <div className="stage-footer">
                <span className="rule-chip chip-purple">Airtight Sanctuary Sealing</span>
              </div>
            </motion.div>
          </div>

          {/* ================= CHRONOLOGICAL TIMELINE MILESTONES ================= */}
          <motion.div
            className="chrono-timeline-section glass-panel"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: 0.25 }}
          >
            <div className="timeline-section-header">
              <div>
                <span className="timeline-kicker">CHRONO-CALIBRATED GAMEPLAN</span>
                <h3 className="timeline-title">Circadian Atmospheric Schedule</h3>
              </div>
              <span className="timeline-target-badge">
                Tailored for {chronoData.persona_title}
              </span>
            </div>

            <div className="timeline-milestones-track">
              {chronoData.schedule.map((slot, index) => {
                let badgeClass = 'badge-normal';
                let icon = <FaCheck />;
                if (slot.level === 'danger') {
                  badgeClass = 'badge-danger';
                  icon = <FaTriangleExclamation />;
                } else if (slot.level === 'optimal') {
                  badgeClass = 'badge-optimal';
                  icon = <FaSun />;
                } else if (slot.level === 'warning') {
                  badgeClass = 'badge-warning';
                  icon = <FaWind />;
                } else if (slot.level === 'safe') {
                  badgeClass = 'badge-safe';
                  icon = <FaShieldVirus />;
                }

                return (
                  <div key={index} className={`timeline-step-row level-${slot.level}`}>
                    <div className="time-col">
                      <span className="step-time">{slot.time}</span>
                    </div>

                    <div className="indicator-col">
                      <div className={`step-node ${badgeClass}`}>
                        {icon}
                      </div>
                      {index < chronoData.schedule.length - 1 && <div className="step-stem"></div>}
                    </div>

                    <div className="content-col">
                      <div className="milestone-title-row">
                        <h4 className="milestone-title">{slot.title}</h4>
                        <span className={`milestone-tag ${badgeClass}`}>
                          {slot.level.toUpperCase()}
                        </span>
                      </div>
                      <p className="milestone-activity">{slot.activity}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>

          {/* ================= AGENTIC 1-CLICK CALENDAR SYNC BAR ================= */}
          <motion.div
            className="calendar-agent-card glass-panel"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: 0.3 }}
          >
            <div className="cal-text-col">
              <div className="cal-icon-wrap">
                <FaCalendarPlus />
              </div>
              <div className="cal-meta">
                <h4 className="cal-title">Agentic Chrono-Calendar Synchronization</h4>
                <p className="cal-desc">
                  Inject today's solar ventilation window and bedroom sanctuary sealing schedule directly into Apple Calendar,
                  Microsoft Outlook, or Google Calendar with zero manual entry.
                </p>
              </div>
            </div>

            <div className="cal-action-buttons">
              <button
                type="button"
                className="btn-cal-download"
                onClick={handleDownloadICS}
                title="Download standard .ics iCalendar file"
              >
                <FaFileArrowDown />
                <span>{copiedCalendar ? 'Downloaded .ICS!' : 'Download .ICS Calendar'}</span>
              </button>

              <a
                href={getGoogleCalendarURL()}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-cal-google"
                title="Add solar aeration window to Google Calendar"
              >
                <span>Google Calendar</span>
                <FaArrowUpRightFromSquare className="ext-icon" />
              </a>
            </div>
          </motion.div>
        </div>
      ) : null}
    </div>
  );
}
