import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaHouseChimney,
  FaCouch,
  FaBed,
  FaUtensils,
  FaChild,
  FaLaptop,
  FaHammer,
  FaSeedling,
  FaCheck,
  FaShieldVirus,
  FaSun,
  FaDroplet,
} from 'react-icons/fa6';
import { fetchIndoorTips, fetchDIYProjects, fetchPlants } from '../utils/api';
import './IndoorHacks.css';

export default function IndoorHacks() {
  const [selectedRoom, setSelectedRoom] = useState('living');
  const [tips, setTips] = useState([]);
  const [diyProjects, setDiyProjects] = useState([]);
  const [plants, setPlants] = useState([]);
  const [loadingTips, setLoadingTips] = useState(true);

  const rooms = [
    { id: 'living', icon: FaCouch, label: 'Living Room', estReduction: '-65% PM2.5' },
    { id: 'bedroom', icon: FaBed, label: 'Master Bedroom', estReduction: '-80% Nocturnal PM' },
    { id: 'kitchen', icon: FaUtensils, label: 'Kitchen & Dining', estReduction: '-90% NO₂ Spikes' },
    { id: 'kids', icon: FaChild, label: "Kids' Bedroom", estReduction: '-85% Exposure' },
    { id: 'office', icon: FaLaptop, label: 'Home Office / Study', estReduction: '< 600 ppm CO₂' },
  ];

  useEffect(() => {
    setLoadingTips(true);
    fetchIndoorTips(selectedRoom)
      .then((res) => {
        setTips(res.data || []);
        setLoadingTips(false);
      })
      .catch((err) => {
        console.error('Failed to fetch indoor tips', err);
        setLoadingTips(false);
      });
  }, [selectedRoom]);

  useEffect(() => {
    fetchDIYProjects()
      .then((res) => setDiyProjects(res.data || []))
      .catch((err) => console.error('Failed to load DIY projects', err));

    fetchPlants()
      .then((res) => setPlants(res.data || []))
      .catch((err) => console.error('Failed to load plants', err));
  }, []);

  return (
    <div className="section" id="indoor">
      {/* Section Header */}
      <div className="section-header">
        <div className="header-badge-row">
          <span className="chrono-badge" style={{ background: 'rgba(6, 182, 212, 0.15)', borderColor: 'rgba(6, 182, 212, 0.35)', color: '#38bdf8' }}>
            <FaShieldVirus /> Indoor Micro-Climate Defense
          </span>
          <span className="target-city-badge">
            WHO Indoor Guideline: &lt; 15 μg/m³ PM2.5
          </span>
        </div>
        <h2>
          <FaHouseChimney /> Indoor Air Quality Hacks
        </h2>
        <p className="section-desc">
          Without protection, outdoor smog permeates indoors through wall fissures and door clearances within 45 minutes.
          Transform your home into an airtight clean-air sanctuary using room-specific airflow tactics and low-cost hospital-grade DIY filtration.
        </p>
      </div>

      <div className="indoor-container">
        {/* Room Selector Strip */}
        <div className="room-nav-wrapper">
          <div className="room-nav-strip">
            {rooms.map((room) => {
              const Icon = room.icon;
              const isSelected = selectedRoom === room.id;
              return (
                <button
                  key={room.id}
                  type="button"
                  className={`room-select-tab ${isSelected ? 'active' : ''}`}
                  onClick={() => setSelectedRoom(room.id)}
                >
                  <Icon className="room-icon" />
                  <div className="room-tab-text">
                    <span className="room-tab-title">{room.label}</span>
                    <span className="room-tab-stat">{room.estReduction}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Room Tips Grid */}
        <div className="room-tips-section">
          {loadingTips ? (
            <div className="loading-state-card">
              <div className="loader-ring"></div>
              <span>Calibrating airflow vectors for this space...</span>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              <motion.div
                key={selectedRoom}
                className="room-tips-grid"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.35 }}
              >
                {tips.map((tip, idx) => (
                  <div key={idx} className="room-tip-card glass-panel">
                    <div className="tip-header-row">
                      <span className="tip-emoji-badge">{tip.emoji || '💡'}</span>
                      <div className="tip-title-box">
                        <h4 className="tip-heading">{tip.title}</h4>
                        <span
                          className={`difficulty-pill ${
                            (tip.difficulty || 'easy').toLowerCase() === 'moderate'
                              ? 'medium'
                              : (tip.difficulty || 'easy').toLowerCase()
                          }`}
                        >
                          {tip.difficulty} setup
                        </span>
                      </div>
                    </div>

                    <p className="tip-body">{tip.description}</p>

                    {tip.impact_text && (
                      <div className="tip-impact-row">
                        <FaCheck className="check-icon" />
                        <span>{tip.impact_text}</span>
                      </div>
                    )}
                  </div>
                ))}
              </motion.div>
            </AnimatePresence>
          )}
        </div>

        {/* DIY Projects Section */}
        <div className="diy-projects-section">
          <div className="sub-header-row">
            <div>
              <h3>
                <FaHammer className="icon-hammer" /> Low-Cost DIY Air Purification Systems
              </h3>
              <p className="sub-caption">
                Commercial HEPA units can cost hundreds of dollars. Build high-CADR particulate filters for under $30 with off-the-shelf components.
              </p>
            </div>
          </div>

          <div className="diy-grid">
            {diyProjects.map((project, idx) => (
              <div key={idx} className="diy-project-card glass-panel">
                <div className="diy-header">
                  <span className="diy-icon-tag">{project.emoji || '🛠️'}</span>
                  <div>
                    <h4>{project.title}</h4>
                    {project.effectiveness && (
                      <span className="diy-cad-badge">⚡ {project.effectiveness}</span>
                    )}
                  </div>
                </div>

                <p className="diy-description">{project.description}</p>

                {project.materials && project.materials.length > 0 && (
                  <div className="materials-wrapper">
                    <span className="mat-caption">Bill of Materials:</span>
                    <div className="materials-pill-list">
                      {project.materials.map((mat, mIdx) => (
                        <span key={mIdx} className="mat-chip">
                          {mat}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Air-Purifying Plants Guide */}
        <div className="plants-guide-section">
          <div className="sub-header-row">
            <div>
              <h3>
                <FaSeedling className="icon-seedling" /> NASA Clean Air Study — Bio-Filtration Houseplants
              </h3>
              <p className="sub-caption">
                While mechanical HEPA filters capture solid PM2.5, plants absorb gaseous formaldehyde, benzene, xylene, and ammonia through root-microbe symbiosis.
              </p>
            </div>
          </div>

          <div className="plants-grid">
            {plants.map((plant, idx) => (
              <div key={idx} className="plant-botanic-card glass-panel">
                <div className="plant-top-row">
                  <span className="plant-avatar">{plant.emoji || '🌿'}</span>
                  <div className="plant-headline">
                    <h4>{plant.name}</h4>
                    {plant.care_level && (
                      <span className="care-tag">Care: {plant.care_level}</span>
                    )}
                  </div>
                </div>

                <p className="plant-desc">{plant.description}</p>

                {plant.benefits && plant.benefits.length > 0 && (
                  <div className="benefits-container">
                    <span className="benefit-caption">Target Air Toxins:</span>
                    <div className="benefits-pills">
                      {plant.benefits.map((b, bIdx) => (
                        <span key={bIdx} className="benefit-chip">
                          ✓ {b}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
