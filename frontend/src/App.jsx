import React, { useState } from 'react';
import { fetchAQI } from './utils/api';
import Hero from './components/Hero';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import ChronoIntelligence from './components/ChronoIntelligence';
import DailyRoutines from './components/DailyRoutines';
import IndoorHacks from './components/IndoorHacks';
import Alternatives from './components/Alternatives';
import ImpactCalculator from './components/ImpactCalculator';
import AIChatPanel from './components/AIChatPanel';
import './App.css';

export default function App() {
  const [isSetup, setIsSetup] = useState(false);
  const [currentSection, setCurrentSection] = useState('dashboard');
  const [city, setCity] = useState('');
  const [lifestyle, setLifestyle] = useState('family');
  const [aqiData, setAqiData] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [setupError, setSetupError] = useState(null);

  const handleSetup = async (selectedCity, selectedLifestyle) => {
    setIsLoading(true);
    setSetupError(null);
    setCity(selectedCity);
    setLifestyle(selectedLifestyle);

    try {
      const res = await fetchAQI(selectedCity);
      if (!res.data || typeof res.data.aqi === 'undefined') {
        throw new Error('Incomplete data received from atmospheric service.');
      }
      setAqiData(res.data);
      setIsSetup(true);
      setCurrentSection('dashboard');
    } catch (err) {
      console.error('Failed to fetch AQI data:', err);
      // B1 FIX: Do NOT fabricate data with fake 165 AQI. Show an error banner with a retry button and no numbers.
      const errMsg =
        err.response?.data?.detail ||
        `Unable to retrieve atmospheric telemetry for "${selectedCity}". Please ensure the backend server is reachable and try again.`;
      setSetupError(errMsg);
      setIsSetup(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigate = (section) => {
    setCurrentSection(section);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderSection = () => {
    switch (currentSection) {
      case 'dashboard':
        return <Dashboard city={city} aqiData={aqiData} />;
      case 'chrono':
        return <ChronoIntelligence city={city} lifestyle={lifestyle} aqiData={aqiData} />;
      case 'routines':
        return <DailyRoutines city={city} lifestyle={lifestyle} aqiData={aqiData} />;
      case 'indoor':
        return <IndoorHacks />;
      case 'alternatives':
        return <Alternatives />;
      case 'impact':
        return <ImpactCalculator />;
      default:
        return <Dashboard city={city} aqiData={aqiData} />;
    }
  };

  if (!isSetup) {
    return (
      <>
        {isLoading && (
          <div className="loading-overlay">
            <div className="loading-content">
              <div className="loading-spinner"></div>
              <p>Connecting to atmospheric telemetry services for {city}...</p>
            </div>
          </div>
        )}
        <Hero
          onSetup={handleSetup}
          setupError={setupError}
          onClearError={() => setSetupError(null)}
          onRetry={() => city && handleSetup(city, lifestyle)}
        />
      </>
    );
  }

  return (
    <div className="app-root">
      <Navbar
        currentSection={currentSection}
        onNavigate={handleNavigate}
        onToggleChat={() => setIsChatOpen(!isChatOpen)}
        city={aqiData?.city || city}
        onChangeCity={() => {
          setIsSetup(false);
          setSetupError(null);
        }}
      />

      <main className="app-container">
        {renderSection()}
      </main>

      <AIChatPanel
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        city={city}
        lifestyle={lifestyle}
        aqiData={aqiData}
      />
    </div>
  );
}
