import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  FaChartLine,
  FaLocationDot,
  FaClock,
  FaDatabase,
  FaShieldHeart,
  FaChartArea,
  FaArrowsRotate,
  FaTriangleExclamation,
  FaCircleCheck,
} from 'react-icons/fa6';
import { fetchForecast } from '../utils/api';
import './Dashboard.css';

function getAqiDetails(aqi) {
  if (aqi <= 50) {
    return {
      label: 'Good',
      color: '#10b981',
      glow: 'rgba(16, 185, 129, 0.4)',
      gradient: 'linear-gradient(135deg, #10b981, #059669)',
      badgeClass: 'good',
      summary: 'Air quality poses little to no risk. Optimal window for outdoor activities and fresh air ventilation.',
    };
  }
  if (aqi <= 100) {
    return {
      label: 'Moderate',
      color: '#eab308',
      glow: 'rgba(234, 179, 8, 0.4)',
      gradient: 'linear-gradient(135deg, #eab308, #ca8a04)',
      badgeClass: 'moderate',
      summary: 'Air quality is acceptable. Very sensitive individuals may experience slight respiratory irritation.',
    };
  }
  if (aqi <= 150) {
    return {
      label: 'Unhealthy for Sensitive Groups',
      color: '#f97316',
      glow: 'rgba(249, 115, 22, 0.45)',
      gradient: 'linear-gradient(135deg, #f97316, #ea580c)',
      badgeClass: 'unhealthy-sg',
      summary: 'Children, asthmatics, and seniors should limit strenuous outdoor play and prolonged exertion.',
    };
  }
  if (aqi <= 200) {
    return {
      label: 'Unhealthy',
      color: '#ef4444',
      glow: 'rgba(239, 68, 68, 0.5)',
      gradient: 'linear-gradient(135deg, #ef4444, #dc2626)',
      badgeClass: 'unhealthy',
      summary: 'Increased likelihood of adverse respiratory symptoms across the population. Outdoor sports should move indoors.',
    };
  }
  if (aqi <= 300) {
    return {
      label: 'Very Unhealthy',
      color: '#8b5cf6',
      glow: 'rgba(139, 92, 246, 0.55)',
      gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
      badgeClass: 'very-unhealthy',
      summary: 'Health alert: significant health risk for everyone. N95 respirators required outdoors; continuous HEPA recommended.',
    };
  }
  // B23 FIX: Unified standardized Hazardous color (#7e0023)
  return {
    label: 'Hazardous',
    color: '#7e0023',
    glow: 'rgba(126, 0, 35, 0.65)',
    gradient: 'linear-gradient(135deg, #7e0023, #4c0519)',
    badgeClass: 'hazardous',
    summary: 'Emergency health warning: serious risk of severe respiratory and cardiovascular effects for the entire population.',
  };
}

export default function Dashboard({ city, aqiData }) {
  const [forecast, setForecast] = useState([]);
  const [loadingForecast, setLoadingForecast] = useState(true);
  const [forecastError, setForecastError] = useState(null);

  const loadForecast = () => {
    if (city) {
      setLoadingForecast(true);
      setForecastError(null);
      fetchForecast(city)
        .then((res) => {
          if (!res.data || res.data.length === 0) {
            throw new Error('No forecast data returned');
          }
          setForecast(res.data);
          setLoadingForecast(false);
        })
        .catch((err) => {
          console.error('Failed to load forecast', err);
          // B9 FIX: Explicit error state when forecast fails instead of empty silent card
          setForecastError('Unable to load hourly forecast for this location.');
          setLoadingForecast(false);
        });
    }
  };

  useEffect(() => {
    loadForecast();
  }, [city]);

  if (!aqiData) {
    return (
      <div className="section loading-state">
        <div className="telemetry-loader">
          <div className="loader-ring"></div>
          <p>Calibrating atmospheric telemetry for {city}...</p>
        </div>
      </div>
    );
  }

  // B7 FIX: Use nullish coalescing ?? so a legitimate 0 is preserved!
  const aqiVal = aqiData.aqi ?? 0;
  const aqiInfo = getAqiDetails(aqiVal);

  // SVG circular arc (circumference = 2 * PI * 85 ~= 534)
  const circumference = 534;
  const strokeOffset = circumference - (circumference * Math.min(aqiVal, 500)) / 500;

  const pollutants = [
    {
      name: 'PM2.5',
      label: 'Fine Particulate Matter',
      value: aqiData.pm25 ?? 0,
      unit: 'μg/m³',
      whoLimit: 15,
      desc: 'Penetrates deep into lungs and bloodstream',
    },
    {
      name: 'PM10',
      label: 'Coarse Particulates',
      value: aqiData.pm10 ?? 0,
      unit: 'μg/m³',
      whoLimit: 45,
      desc: 'Dust, pollen, and construction particulates',
    },
    {
      name: 'NO₂',
      label: 'Nitrogen Dioxide',
      value: aqiData.no2 ?? 0,
      unit: 'μg/m³',
      whoLimit: 25,
      desc: 'Vehicle exhaust and combustion byproduct',
    },
    {
      name: 'SO₂',
      label: 'Sulphur Dioxide',
      value: aqiData.so2 ?? 0,
      unit: 'μg/m³',
      whoLimit: 40,
      desc: 'Industrial emissions & coal combustion',
    },
    {
      name: 'CO',
      label: 'Carbon Monoxide',
      value: aqiData.co ?? 0,
      unit: 'mg/m³',
      whoLimit: 4,
      desc: 'Incomplete combustion; reduces oxygen transport',
    },
    {
      name: 'O₃',
      label: 'Surface Ozone',
      value: aqiData.o3 ?? 0,
      unit: 'μg/m³',
      whoLimit: 100,
      desc: 'Secondary photochemical smog pollutant',
    },
  ];

  return (
    <div className="section" id="dashboard">
      {/* Dashboard Header */}
      <div className="dashboard-header-container">
        <div>
          <div className="dashboard-status-row">
            {/* B27 FIX: Accurate, factual data source descriptions */}
            {aqiData.is_realtime ? (
              <span className="live-status-pill">
                <span className="live-pulsing-dot"></span>
                <span>HOURLY REANALYSIS & SENSOR FEED</span>
              </span>
            ) : (
              <span className="baseline-status-pill">
                <span>CALIBRATED REGIONAL BASELINE MODEL</span>
              </span>
            )}
            <span className="data-timestamp">
              <FaClock /> {aqiData.last_updated || 'Live Station Feed'}
            </span>
          </div>

          <h2 className="dashboard-main-title">
            <FaChartLine className="title-icon" />
            <span>Air Quality Telemetry</span>
          </h2>
        </div>

        <div className="location-pill-card">
          <FaLocationDot className="loc-pin" />
          <div className="loc-text-col">
            <span className="loc-city">{aqiData.city || city}</span>
            <span className="loc-status">{aqiData.category || aqiInfo.label}</span>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="dashboard-grid">
        {/* ================= HERO AQI GAUGE CARD ================= */}
        <motion.div
          className="aqi-primary-hero-card glass-panel"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          style={{ '--card-glow': aqiInfo.glow }}
        >
          {/* Dial Visualizer */}
          <div className="aqi-gauge-col">
            <div className="aqi-gauge-wrapper">
              <svg
                className="aqi-svg-ring"
                viewBox="0 0 200 200"
                width="220"
                height="220"
                style={{ width: '220px', height: '220px', display: 'block' }}
              >
                <circle
                  cx="100"
                  cy="100"
                  r="85"
                  className="aqi-ring-track"
                  fill="none"
                  strokeWidth="12"
                  style={{ fill: 'none' }}
                />
                <circle
                  cx="100"
                  cy="100"
                  r="85"
                  className="aqi-ring-meter"
                  fill="none"
                  strokeWidth="12"
                  stroke={aqiInfo.color}
                  strokeDasharray={circumference}
                  strokeDashoffset={strokeOffset}
                  strokeLinecap="round"
                  style={{
                    fill: 'none',
                    filter: `drop-shadow(0 0 10px ${aqiInfo.color})`,
                    transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1)',
                  }}
                />
              </svg>

              <div className="aqi-center-display">
                <span className="aqi-index-title">AIR QUALITY</span>
                <span className="aqi-index-number" style={{ color: aqiInfo.color }}>
                  {aqiVal}
                </span>
                <span
                  className="aqi-status-tag"
                  style={{
                    background: `${aqiInfo.color}22`,
                    color: aqiInfo.color,
                    border: `1px solid ${aqiInfo.color}55`,
                  }}
                >
                  {aqiData.category || aqiInfo.label}
                </span>
              </div>
            </div>
          </div>

          {/* Text Summary */}
          <div className="aqi-narrative-col">
            <div className="category-pill-wrapper">
              <span
                className="category-hero-pill"
                style={{ background: aqiInfo.gradient, color: '#fff' }}
              >
                {aqiData.category || aqiInfo.label}
              </span>
              <span className="aqi-scale-indicator">Standard Scale: 0 - 500 Index</span>
            </div>

            <p className="aqi-narrative-text">
              {aqiData.health_advisory || aqiInfo.summary}
            </p>

            <div className="aqi-meta-grid">
              <div className="meta-box">
                <span className="m-label">PRIMARY POLLUTANT</span>
                <span className="m-val" style={{ color: aqiInfo.color }}>
                  PM2.5 ({aqiData.pm25 ?? 0} μg/m³)
                </span>
              </div>
              <div className="meta-box">
                <span className="m-label">DATA SOURCE</span>
                <span className="m-val">
                  <FaDatabase /> {aqiData.source || 'Open-Meteo Sensor Feed'}
                </span>
              </div>
              <div className="meta-box">
                <span className="m-label">HEALTH RISK RATING</span>
                <span className="m-val warning">
                  {aqiVal > 100 ? 'Elevated Vulnerability' : 'Low Exposure Risk'}
                </span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* ================= MULTI-POLLUTANT BREAKDOWN ================= */}
        <div className="pollutant-matrix-section">
          <div className="sub-header-row">
            <h3>🔬 Detailed Pollutant Matrix</h3>
            <span className="sub-caption">Real-time concentrations vs. WHO Safety Guidelines</span>
          </div>

          <div className="pollutant-grid">
            {pollutants.map((p) => {
              const timesWho = (p.value / p.whoLimit).toFixed(1);
              const isOver = p.value > p.whoLimit;
              const fillRatio = Math.min((p.value / (p.whoLimit * 3.5)) * 100, 100);

              return (
                <div key={p.name} className="pollutant-matrix-card">
                  <div className="pollutant-top">
                    <span className="p-tag">{p.name}</span>
                    <span className={`who-badge ${isOver ? 'danger' : 'safe'}`}>
                      {isOver ? `${timesWho}x WHO Limit` : '✓ Within WHO'}
                    </span>
                  </div>

                  <div className="pollutant-num-row">
                    <span className="p-big-val">{p.value}</span>
                    <span className="p-unit-tag">{p.unit}</span>
                  </div>

                  <div className="pollutant-subname">{p.label}</div>

                  <div className="p-progress-track">
                    <div
                      className="p-progress-bar"
                      style={{
                        width: `${Math.max(fillRatio, 6)}%`,
                        background: isOver
                          ? 'linear-gradient(90deg, #f59e0b, #ef4444)'
                          : 'linear-gradient(90deg, #10b981, #34d399)',
                      }}
                    />
                  </div>

                  <div className="p-footer-desc">{p.desc}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ================= 24-HOUR FORECAST CHART (B9 FIX) ================= */}
        <div className="forecast-card glass-panel">
          <div className="forecast-header-row">
            <div>
              <h3>
                <FaChartArea className="chart-icon" /> 24-Hour Smog & Particulate Forecast
              </h3>
              <p className="chart-subtext">
                Diurnal atmospheric modeling: temperature inversions concentrate surface smog during dawn and dusk.
              </p>
            </div>
            {aqiVal > 150 && (
              <div className="inversion-alert-pill">
                <FaTriangleExclamation /> Elevated morning inversion expected
              </div>
            )}
          </div>

          {loadingForecast ? (
            <div className="forecast-loading">
              <div className="loading-spinner-sm"></div>
              <span>Fetching predictive hourly atmospheric vectors...</span>
            </div>
          ) : forecastError ? (
            <div className="forecast-error-card">
              <FaTriangleExclamation className="forecast-err-icon" />
              <div className="forecast-err-text">
                <strong>Forecast Unavailable</strong>
                <p>{forecastError}</p>
              </div>
              <button type="button" className="forecast-retry-btn" onClick={loadForecast}>
                <FaArrowsRotate /> Retry
              </button>
            </div>
          ) : (
            <div className="forecast-timeline-container">
              <div className="forecast-chart-area">
                {forecast.map((item, idx) => {
                  const maxChartAqi = 360;
                  const heightPercent = Math.min((item.aqi / maxChartAqi) * 100, 100);
                  const isHourHigh = item.aqi > 150;

                  return (
                    <div key={idx} className="forecast-column">
                      <div className="forecast-bar-track">
                        <div
                          className="forecast-dynamic-bar"
                          style={{
                            height: `${Math.max(heightPercent, 8)}%`,
                            background: item.color || '#3b82f6',
                            boxShadow: isHourHigh ? `0 0 10px ${item.color}66` : 'none',
                          }}
                        >
                          <div className="bar-hover-tooltip">
                            <div className="tip-time">{item.hour}</div>
                            <div className="tip-aqi">AQI {item.aqi}</div>
                          </div>
                        </div>
                      </div>
                      <span className="forecast-hour-label">{item.hour}</span>
                    </div>
                  );
                })}
              </div>

              {/* Legend Bar */}
              <div className="forecast-scale-legend">
                <span className="leg-item good">Good (0-50)</span>
                <span className="leg-item moderate">Moderate (51-100)</span>
                <span className="leg-item usg">Sensitive (101-150)</span>
                <span className="leg-item unhealthy">Unhealthy (151-200)</span>
                <span className="leg-item very-unhealthy">Very Unhealthy (201-300)</span>
                <span className="leg-item hazardous">Hazardous (301+)</span>
              </div>
            </div>
          )}
        </div>

        {/* ================= CLINICAL HEALTH ADVISORY ================= */}
        <div className="advisory-card glass-panel">
          <div className="advisory-header">
            <FaShieldHeart className="adv-main-icon" />
            <div>
              <h3>Protective Protocols & Smog Precautions</h3>
              <p>Actionable recommendations calibrated to current airborne particulate density.</p>
            </div>
          </div>

          <div className="advisory-content">
            <div className="advisory-item">
              <div className="adv-icon-badge">😷</div>
              <div className="adv-body">
                <strong>Respiratory Barrier Defense</strong>
                <p>
                  {aqiVal > 150
                    ? 'Wear an airtight N95/N99 respirator outdoors. Standard surgical masks fail against PM2.5 particulates.'
                    : 'A cloth or light mask is sufficient during short walks; sensitive individuals should wear an N95 near major arterial traffic.'}
                </p>
              </div>
            </div>

            <div className="advisory-item">
              <div className="adv-icon-badge">🏠</div>
              <div className="adv-body">
                <strong>Indoor Sanctuary Management</strong>
                <p>
                  Keep doors and windows firmly sealed during dawn and dusk inversions. Run True HEPA purifiers continuously in bedrooms.
                </p>
              </div>
            </div>

            <div className="advisory-item">
              <div className="adv-icon-badge">🏃</div>
              <div className="adv-body">
                <strong>Exercise & Cardio Timing</strong>
                <p>
                  {aqiVal > 150
                    ? 'Avoid all outdoor cardiovascular training. High exertion draws fine soot deep into bronchial airways.'
                    : 'Schedule outdoor runs or cycle rides strictly during midday (1:00 PM - 3:30 PM) when convective mixing disperses pollutants.'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
