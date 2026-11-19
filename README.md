# 🌬️ BreatheEasy — AI-Powered Clean Air Companion

A GenAI-powered assistant that helps families and communities navigate severe winter smog and urban air pollution. Built with **Python (FastAPI)** backend and **React (Vite)** frontend.

## 🌟 Features

- **🌍 Air Quality Dashboard** — Real-time atmospheric telemetry via Open-Meteo, 24-hour diurnal inversion forecast, multi-pollutant matrix (PM2.5, PM10, NO₂, SO₂, CO, O₃), and clinical health protocols.
- **📅 Low-Emission Daily Routines** — Chrono-atmospheric schedules tailored to 7 demographic profiles (Families with Children, Seniors, Commuters, Students, WFH, Athletes, Outdoor Workers) shifting exposure away from winter morning inversions.
- **🏠 Indoor Air Quality Hacks** — Room-by-room sealed sanctuary tips, hospital-grade DIY air purifier blueprints (Corsi-Rosenthal Box), and NASA Clean Air botanical bio-filters.
- **🌱 Sustainable Alternatives** — Replace pollution-heavy habits with cleaner choices across transport, cooking, heating, shopping, waste, and energy with quantified CO₂ reductions.
- **📊 Impact Calculator & Community Pledges** — Real-time calculation comparing household choices against regional baselines, tangible environmental equivalents, and interactive community pledges that persist dynamically.
- **💬 AI Chat Assistant** — Dual-engine advisory powered by Google Gemini 2.0 Flash (with timeout protection, per-request key support, conversation memory, and markdown rendering) backed by a verified clinical rule engine with whole-word matching.

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn, Pydantic, python-dotenv |
| Frontend | React 18, Vite, Framer Motion, Axios, React Icons |
| AI Reasoning | Google Gemini 2.0 Flash + Clinical Clean Air Rule Engine |
| Atmospheric Data | Open-Meteo Air Quality & Geocoding APIs (with in-memory TTL caching) |
| Testing | Python `unittest` + FastAPI `TestClient` |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env   # (Optional) Add your Gemini key
python main.py
```
Backend runs at `http://localhost:8000`.

To run the automated backend test suite:
```bash
python -m unittest test_api.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:3000`.

### 3. Optional: Enable Gemini 2.0 Flash
Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey):
```bash
export GEMINI_API_KEY="your_api_key_here"
```
Or enter your key directly into the in-app chat settings dialog. Without a key or when offline, BreatheEasy automatically runs on its clinical rule engine.

## 📁 Project Structure

```
Challenge 6/
├── .env.example             # Example environment variables
├── .gitignore               # Ignored dependencies, caches, and build artifacts
├── run.sh                   # Startup launcher for backend & frontend
├── README.md                # Documentation and architecture guide
├── backend/
│   ├── main.py              # FastAPI server with 11 endpoints, caching, and validation
│   ├── data.py              # Curated datasets for 17 global metropolises, rooms, and DIY hacks
│   ├── ai_assistant.py      # Gemini 2.0 Flash integration + whole-word clinical fallback
│   ├── test_api.py          # Automated test suite
│   └── requirements.txt     # Python backend dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx          # Root application router with error boundaries
    │   ├── main.jsx         # React DOM entry point
    │   ├── components/
    │   │   ├── Hero.jsx             # Haute landing page with real geolocation detection
    │   │   ├── Navbar.jsx           # Responsive floating jewel navigation bar
    │   │   ├── Dashboard.jsx        # AQI telemetry dial, pollutant matrix, and 24h forecast
    │   │   ├── DailyRoutines.jsx    # Chrono-smart routines with request race prevention
    │   │   ├── IndoorHacks.jsx      # Room-specific hacks & DIY Corsi-Rosenthal blueprints
    │   │   ├── Alternatives.jsx     # Side-by-side sustainable substitutions
    │   │   ├── ImpactCalculator.jsx # Dynamic emission simulator & community pledge wall
    │   │   └── AIChatPanel.jsx      # AI copilot with markdown and conversational memory
    │   └── utils/api.js             # Axios API client
    ├── package.json
    └── vite.config.js
```

## 🌍 Supported Metropolises

Delhi, Tokyo, Beijing, Lahore, Dhaka, Cairo, Mumbai, Kolkata, Karachi, Jakarta, Hanoi, Kathmandu, London, Paris, New York, Los Angeles, Sydney — and any global city via live reverse geocoding and atmospheric feeds.

---

*Built for cleaner air, resilient families, and empowered communities* 🌿
