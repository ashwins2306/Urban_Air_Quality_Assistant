import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FaLeaf,
  FaPeopleGroup,
  FaArrowRight,
  FaHeartPulse,
  FaWallet,
  FaTree,
  FaCheck,
  FaBicycle,
  FaFireBurner,
  FaTemperatureArrowUp,
  FaRecycle,
  FaBolt,
} from 'react-icons/fa6';
import { fetchAlternatives, fetchCommunity } from '../utils/api';
import './Alternatives.css';

export default function Alternatives() {
  const [category, setCategory] = useState('all');
  const [alternatives, setAlternatives] = useState([]);
  const [community, setCommunity] = useState([]);
  const [loading, setLoading] = useState(true);

  const categories = [
    { id: 'all', label: 'All Habits', icon: FaLeaf },
    { id: 'transport', label: 'Transport', icon: FaBicycle },
    { id: 'cooking', label: 'Cooking', icon: FaFireBurner },
    { id: 'heating', label: 'Space Heating', icon: FaTemperatureArrowUp },
    { id: 'shopping', label: 'Shopping', icon: FaLeaf },
    { id: 'waste', label: 'Waste Circularity', icon: FaRecycle },
    { id: 'energy', label: 'Clean Energy', icon: FaBolt },
  ];

  useEffect(() => {
    setLoading(true);
    fetchAlternatives(category)
      .then((res) => {
        setAlternatives(res.data || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load alternatives', err);
        setLoading(false);
      });
  }, [category]);

  useEffect(() => {
    fetchCommunity()
      .then((res) => setCommunity(res.data || []))
      .catch((err) => console.error('Failed to load community initiatives', err));
  }, []);

  return (
    <div className="section" id="alternatives">
      {/* Header */}
      <div className="section-header">
        <div className="header-badge-row">
          <span className="chrono-badge" style={{ background: 'rgba(16, 185, 129, 0.15)', borderColor: 'rgba(16, 185, 129, 0.35)', color: '#34d399' }}>
            <FaLeaf /> Sustainable Lifestyle Substitution
          </span>
          <span className="target-city-badge">
            Direct Carbon & Smog Mitigation
          </span>
        </div>
        <h2>
          <FaLeaf /> Sustainable Alternatives & Green Swaps
        </h2>
        <p className="section-desc">
          Severe winter pollution is intensely magnified by everyday micro-actions: cold engine idling, solid fuel burning, unvented heating, and municipal waste dumping.
          Adopt these science-backed lifestyle substitutions that slash emissions while protecting your family's health and budget.
        </p>
      </div>

      <div className="alternatives-container">
        {/* Category Filter Pills */}
        <div className="alt-category-strip">
          {categories.map((cat) => {
            const Icon = cat.icon;
            const isSelected = category === cat.id;
            return (
              <button
                key={cat.id}
                type="button"
                className={`alt-category-pill ${isSelected ? 'active' : ''}`}
                onClick={() => setCategory(cat.id)}
              >
                <Icon className="cat-icon" />
                <span>{cat.label}</span>
              </button>
            );
          })}
        </div>

        {/* Alternatives Card Deck */}
        <div className="alternatives-deck-section">
          {loading ? (
            <div className="loading-state-card">
              <div className="loader-ring"></div>
              <span>Evaluating sustainable habit substitutions...</span>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              <motion.div
                key={category}
                className="alternatives-grid"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.35 }}
              >
                {alternatives.map((item, idx) => (
                  <div key={idx} className={`alt-card glass-panel cat-${item.category || 'transport'}`}>
                    {/* Top Accent Strip */}
                    <div className="alt-card-top">
                      <span className="alt-emoji-box">{item.emoji || '🌱'}</span>
                      {item.co2_savings && (
                        <span className="alt-savings-badge">
                          <FaTree className="tree-icon" /> {item.co2_savings}
                        </span>
                      )}
                    </div>

                    <h4 className="alt-card-title">{item.title}</h4>

                    {/* Swap Visualizer */}
                    <div className="alt-swap-container">
                      <div className="swap-side old">
                        <span className="swap-badge">CONVENTIONAL</span>
                        <div className="swap-desc-text">{item.swap_from}</div>
                      </div>

                      <div className="swap-transition-arrow">
                        <FaArrowRight />
                      </div>

                      <div className="swap-side new">
                        <span className="swap-badge">GREEN ALTERNATIVE</span>
                        <div className="swap-desc-text">{item.swap_to}</div>
                      </div>
                    </div>

                    <p className="alt-narrative">{item.description}</p>

                    {/* Direct Impact Row */}
                    <div className="alt-impact-footer">
                      {item.health_impact && (
                        <div className="impact-pill health">
                          <FaHeartPulse className="pill-icon" />
                          <span>{item.health_impact}</span>
                        </div>
                      )}
                      {item.cost_impact && (
                        <div className="impact-pill cost">
                          <FaWallet className="pill-icon" />
                          <span>{item.cost_impact}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </motion.div>
            </AnimatePresence>
          )}
        </div>

        {/* Urban Greenery & Forestry Spotlight */}
        <div className="nature-canopy-spotlight glass-panel">
          <div className="canopy-spotlight-img-wrap">
            <img
              src="/nature/clean-forest-canopy.svg"
              alt="Community Urban Forest & Green Canopy"
              className="canopy-spotlight-img"
            />
          </div>
          <div className="canopy-spotlight-content">
            <div className="canopy-spotlight-badge">
              <FaTree /> Urban Forestry & Bio-Sanctuaries
            </div>
            <h3>Community Tree Canopies & Green Corridors</h3>
            <p>
              Dense urban foliage and bioswales settle airborne particulate matter by up to 24% while creating natural cooling micro-climates that disrupt thermal inversion traps.
            </p>
          </div>
        </div>

        {/* Community Initiatives */}
        <div className="community-collective-section">
          <div className="sub-header-row">
            <div>
              <h3>
                <FaPeopleGroup className="icon-people" /> Collective & Neighborhood Actions
              </h3>
              <p className="sub-caption">
                Individual changes scale exponentially when an entire apartment complex or neighborhood acts in unison.
              </p>
            </div>
          </div>

          <div className="community-grid">
            {community.map((comm, idx) => (
              <div key={idx} className="community-card glass-panel">
                <div className="community-header">
                  <span className="comm-emoji-tag">{comm.emoji || '🤝'}</span>
                  <h4>{comm.title}</h4>
                </div>
                <p>{comm.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
