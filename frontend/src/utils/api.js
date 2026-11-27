import axios from 'axios';

// Connect to deployed backend URL if configured, or localhost:8000 locally
const getBaseURL = () => {
  if (import.meta.env && import.meta.env.VITE_API_URL) {
    const base = import.meta.env.VITE_API_URL.replace(/\/+$/, '');
    return base.endsWith('/api') ? base : `${base}/api`;
  }
  if (typeof window !== 'undefined') {
    const host = window.location.hostname || 'localhost';
    if (host === 'localhost' || host === '127.0.0.1') {
      return `http://${host}:8000/api`;
    }
  }
  return '/api';
};

const API = axios.create({ baseURL: getBaseURL() });

// EPA AQI Standard category determination (zero hardcoded city data)
function getAqiCategoryInfo(aqi) {
  if (aqi <= 50) return { category: 'Good', color: '#10b981', advisory: 'Air quality is satisfactory; air pollution poses little or no risk.' };
  if (aqi <= 100) return { category: 'Moderate', color: '#eab308', advisory: 'Air quality is acceptable; unusually sensitive individuals should consider limiting prolonged outdoor exertion.' };
  if (aqi <= 150) return { category: 'Unhealthy for Sensitive Groups', color: '#f97316', advisory: 'Members of sensitive groups may experience health effects. General public less likely to be affected.' };
  if (aqi <= 200) return { category: 'Unhealthy', color: '#ef4444', advisory: 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.' };
  if (aqi <= 300) return { category: 'Very Unhealthy', color: '#8b5cf6', advisory: 'Health alert: risk of health effects is increased for everyone.' };
  return { category: 'Hazardous', color: '#7e0023', advisory: 'Health warning of emergency conditions: everyone is more likely to be affected.' };
}

// Client-side direct live Open-Meteo fetch when local backend has no external internet
async function fetchDirectOpenMeteoAQI(city) {
  const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;
  const geoRes = await fetch(geoUrl);
  const geoData = await geoRes.json();
  if (!geoData.results || geoData.results.length === 0) {
    throw new Error(`Location '${city}' could not be resolved.`);
  }
  const { latitude, longitude, name, country } = geoData.results[0];
  const aqiUrl = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${latitude}&longitude=${longitude}&current=us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone&timezone=auto`;
  const aqiRes = await fetch(aqiUrl);
  const aqiData = await aqiRes.json();
  const curr = aqiData.current || {};
  const rawAqi = curr.us_aqi;
  if (rawAqi == null) {
    throw new Error(`No atmospheric sensor data available for ${name}.`);
  }
  const aqiVal = Math.round(rawAqi);
  const cat = getAqiCategoryInfo(aqiVal);
  const utcNow = new Date().toISOString().replace('T', ' ').substring(0, 16) + ' UTC';

  return {
    data: {
      city: `${name}${country ? ', ' + country : ''}`,
      aqi: aqiVal,
      category: cat.category,
      color: cat.color,
      pm25: curr.pm2_5 != null ? Math.round(curr.pm2_5 * 10) / 10 : 0,
      pm10: curr.pm10 != null ? Math.round(curr.pm10 * 10) / 10 : 0,
      no2: curr.nitrogen_dioxide != null ? Math.round(curr.nitrogen_dioxide * 10) / 10 : 0,
      so2: curr.sulphur_dioxide != null ? Math.round(curr.sulphur_dioxide * 10) / 10 : 0,
      co: curr.carbon_monoxide != null ? Math.round((curr.carbon_monoxide / 1000) * 100) / 100 : 0,
      o3: curr.ozone != null ? Math.round(curr.ozone * 10) / 10 : 0,
      health_advisory: `${name}: ${cat.advisory}`,
      quick_actions: [],
      is_realtime: true,
      source: 'Open-Meteo Satellite & Sensor Feed (Direct)',
      last_updated: utcNow,
    }
  };
}

async function fetchDirectOpenMeteoForecast(city) {
  const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(city)}&count=1&language=en&format=json`;
  const geoRes = await fetch(geoUrl);
  const geoData = await geoRes.json();
  if (!geoData.results || geoData.results.length === 0) {
    throw new Error(`Location '${city}' could not be resolved.`);
  }
  const { latitude, longitude } = geoData.results[0];
  const fcUrl = `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${latitude}&longitude=${longitude}&hourly=us_aqi&timezone=auto&forecast_days=2`;
  const fcRes = await fetch(fcUrl);
  const fcData = await fcRes.json();
  const hourly = fcData.hourly || {};
  const times = hourly.time || [];
  const aqis = hourly.us_aqi || [];

  const currentHourStr = new Date().toISOString().substring(0, 13) + ':00';
  let startIdx = 0;
  for (let i = 0; i < times.length; i++) {
    if (times[i] >= currentHourStr) {
      startIdx = i;
      break;
    }
  }
  const sliceTimes = times.slice(startIdx, startIdx + 24);
  const sliceAqis = aqis.slice(startIdx, startIdx + 24);
  const points = [];
  for (let i = 0; i < sliceTimes.length; i++) {
    const val = sliceAqis[i] != null ? Math.round(sliceAqis[i]) : 50;
    const cat = getAqiCategoryInfo(val);
    const hourLabel = sliceTimes[i].includes('T') ? sliceTimes[i].split('T')[1].substring(0, 5) : sliceTimes[i];
    points.push({
      hour: hourLabel,
      time: hourLabel,
      aqi: val,
      color: cat.color,
      is_realtime: true,
    });
  }
  return { data: points };
}

export const fetchAQI = async (city) => {
  try {
    return await API.get('/aqi/' + encodeURIComponent(city));
  } catch (err) {
    return await fetchDirectOpenMeteoAQI(city);
  }
};

export const fetchForecast = async (city) => {
  try {
    return await API.get('/forecast/' + encodeURIComponent(city));
  } catch (err) {
    return await fetchDirectOpenMeteoForecast(city);
  }
};

export const fetchRoutines = (city, lifestyle, aqi) => API.post('/routines', { city, lifestyle, aqi });
export const fetchChronoIntelligence = (city, lifestyle, aqi, forecast = null, apiKey = null) =>
  API.post('/chrono-intelligence', { city, lifestyle, aqi, forecast, api_key: apiKey });
export const fetchIndoorTips = (room) => API.get('/indoor-tips/' + encodeURIComponent(room));
export const fetchDIYProjects = () => API.get('/diy-projects');
export const fetchPlants = () => API.get('/plants');
export const fetchAlternatives = (category) => API.get('/alternatives', { params: { category } });
export const fetchCommunity = () => API.get('/community');
export const calculateImpact = (choices) => API.post('/calculate-impact', choices);
export const fetchPledges = () => API.get('/pledges');
export const togglePledge = (id, pledged) => API.post('/pledges', { id, pledged });
export const sendChatMessage = (message, context, apiKey = null, history = []) =>
  API.post('/chat', { message, context, api_key: apiKey, history });

export default API;
