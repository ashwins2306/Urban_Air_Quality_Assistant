# 🌬️ BreatheEasy — AI-Powered Clean Air Companion

A GenAI-powered atmospheric health intelligence assistant that helps families, individuals, and communities navigate severe winter smog, diurnal thermal inversions, and urban air pollution. Built with a high-performance **Python (FastAPI)** backend and a responsive **React (Vite)** frontend.

## 🌟 Key Features

- **🌍 Live Air Quality Telemetry** — Real-time atmospheric data via Open-Meteo hourly reanalysis, 24-hour diurnal inversion forecast, multi-pollutant matrix (PM2.5, PM10, NO₂, SO₂, CO, O₃), and clinical health protocols.
- **⏳ Diurnal Chrono-Intelligence** — Personalized meteorological smog inversion briefings, spoken audio transcripts, and 1-click agentic calendar sync to bypass morning ground radiation inversion traps.
- **📅 Low-Emission Daily Routines** — Chrono-atmospheric schedules tailored to 7 demographic profiles (Families with Children, Seniors, Commuters, Students, WFH, Athletes, Outdoor Workers) shifting exposure away from winter morning inversions.
- **🏠 Indoor Air Quality Hacks & Bio-Filters** — Room-by-room sealed sanctuary tips, hospital-grade DIY air purifier blueprints (Corsi-Rosenthal Box), and NASA Clean Air botanical bio-filters with custom botanical visualizers.
- **🌱 Sustainable Alternatives** — Replace pollution-heavy habits with cleaner choices across transport, cooking, heating, shopping, waste, and energy with quantified CO₂ reductions and urban forestry showcases.
- **📊 Impact Calculator & Community Pledges** — Real-time calculation comparing household choices against regional baselines, tangible environmental equivalents, and interactive community pledges that persist dynamically.
- **💬 Dual-Engine AI Copilot** — Multi-provider advisory powered by **OpenAI (GPT-4o-mini)** and **Google Gemini 2.0 Flash** (with timeout protection, per-request key support, conversation memory, and markdown rendering) backed by a verified clinical rule engine with whole-word matching.

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic, python-dotenv |
| **Frontend** | React 18, Vite, Framer Motion, Axios, React Icons |
| **AI Reasoning** | OpenAI (GPT-4o-mini) + Google Gemini 2.0 Flash + Clinical Clean Air Rule Engine |
| **Atmospheric Data** | Open-Meteo Air Quality & Geocoding APIs (with in-memory TTL caching) |
| **Styling & Assets** | Luxury Obsidian glassmorphic design, vector atmospheric streamlines & botanical SVG suite |
| **Testing** | Python `unittest` + FastAPI `TestClient` |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### 1-Click Launch (Recommended)
You can launch both the backend and frontend simultaneously using the provided startup script:
```bash
./run.sh
```

---

### Manual Launch

#### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env   # (Optional) Add your OpenAI or Gemini key
python main.py
```
Backend runs at `http://localhost:8000`.  
Interactive API Docs available at `http://localhost:8000/docs`.

To run the automated backend test suite:
```bash
python -m unittest test_api.py
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:3000`.

---

### 🔑 Zero-Setup Ready & Optional GenAI Keys

> **Note for Evaluators:**  
> BreatheEasy is **zero-setup ready out-of-the-box**. If no API key is provided, the application automatically runs on its verified Clinical Clean Air Rule Engine and live Open-Meteo atmospheric telemetry without errors.

To unlock advanced generative conversational reasoning with an LLM, you can optionally configure either:

- **OpenAI (GPT-4o-mini)**: Add `OPENAI_API_KEY="sk-..."` in `backend/.env` or enter it directly in the in-app chat dialog.
- **Google Gemini 2.0 Flash**: Add `GEMINI_API_KEY="..."` in `backend/.env` or enter it directly in the in-app chat dialog.

---

## 🌐 Live Deployment via GitHub

This project contains a pre-configured [`render.yaml`](render.yaml) blueprint to deploy both the FastAPI backend and React frontend simultaneously for free.

### Option 1: 1-Click Blueprint on Render.com (Recommended)
1. Push your repository to GitHub.
2. Sign in to [Render.com](https://render.com) using your GitHub account.
3. Click **New +** > **Blueprint**.
4. Select your `Challenge-6` repository and click **Apply**.
5. Render automatically deploys:
   - **`breatheasy-backend`** (FastAPI Web Service)
   - **`breatheasy-frontend`** (React Static Site, automatically wired to the backend URL)

### Option 2: Vercel (Frontend) + Render (Backend)
1. **Backend**: On Render, create a **Web Service**, select `backend`, Build Command: `pip install -r backend/requirements.txt`, Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`. Copy the generated backend URL (`https://...onrender.com`).
2. **Frontend**: On [Vercel.com](https://vercel.com), import your GitHub repo, set Root Directory to `frontend`, add Environment Variable `VITE_API_URL=https://your-backend.onrender.com`, and click **Deploy**.

## 📁 Project Structure

```
Challenge 6/
├── .env.example             # Example environment variables (OpenAI, Gemini, Host/Port)
├── .gitignore               # Configured to exclude node_modules, dist, __pycache__, and secrets
├── run.sh                   # Startup launcher for backend & frontend
├── README.md                # Documentation and architecture guide
├── backend/
│   ├── main.py              # FastAPI server with 11 endpoints, caching, and validation
│   ├── data.py              # Curated datasets for global metropolises, rooms, and DIY blueprints
│   ├── ai_assistant.py      # Dual GenAI (OpenAI & Gemini) integration + clinical rule fallback
│   ├── test_api.py          # Automated test suite (100% passing)
│   └── requirements.txt     # Python backend dependencies
└── frontend/
    ├── public/              # Lightweight vector assets (< 50 KB total)
    │   ├── background.svg   # Minimal clean-air atmospheric streamline background
    │   └── nature/          # NASA botanical bio-filters & alpine sanctuary illustrations
    ├── src/
    │   ├── App.jsx          # Root application router with error boundaries
    │   ├── main.jsx         # React DOM entry point
    │   ├── index.css        # Global luxury obsidian theme & typography
    │   ├── App.css          # Layout styling
    │   ├── components/
    │   │   ├── Hero.jsx                 # Haute landing page with real geolocation & sanctuary visualizer
    │   │   ├── Navbar.jsx               # Responsive floating jewel navigation bar
    │   │   ├── Dashboard.jsx            # AQI telemetry dial, pollutant matrix, and 24h forecast
    │   │   ├── ChronoIntelligence.jsx   # Diurnal inversion briefing & calendar sync
    │   │   ├── DailyRoutines.jsx        # Chrono-smart routines with request race prevention
    │   │   ├── IndoorHacks.jsx          # Room hacks, DIY filters & NASA botanical plant cards
    │   │   ├── Alternatives.jsx         # Sustainable substitutions & urban forestry spotlight
    │   │   ├── ImpactCalculator.jsx     # Dynamic emission simulator & community pledge wall
    │   │   └── AIChatPanel.jsx          # Dual-engine AI copilot with markdown & memory
    │   └── utils/api.js                 # Axios API client
    ├── package.json
    └── vite.config.js
```

## 🌍 Supported Metropolises

Delhi, Mumbai, Bengaluru, Kolkata, Chennai, Hyderabad, Ahmedabad, Pune, Jaipur, Lucknow, Tokyo, Beijing, Lahore, Dhaka, Cairo, London, Paris, New York, Sydney — and any global city via live reverse geocoding and Open-Meteo atmospheric feeds.

---

*Built for cleaner air, resilient families, and empowered communities* 🌿
