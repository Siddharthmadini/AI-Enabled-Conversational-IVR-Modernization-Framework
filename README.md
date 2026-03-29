# 📞 AI-Enabled Conversational IVR Modernization Framework

### IRCTC-Focused Hybrid IVR using ACS, BAP & Conversational AI

🚀 **Live Demo:** [https://ai-enabled-conversational-ivr-moder.vercel.app/](https://ai-enabled-conversational-ivr-moder.vercel.app/)

---

## 🧩 Project Overview

This project modernizes the traditional **IRCTC Interactive Voice Response (IVR)** system by integrating cloud-based conversational AI technologies. Instead of replacing the entire system, it extends the existing **VoiceXML-based IVR** with intelligent conversational capabilities — making it more scalable, flexible, and user-friendly.

The framework demonstrates how legacy IVR systems can be integrated with **Azure Communication Services (ACS)**, **Twilio**, and **Bot Application Platforms (BAP)** to enable natural language interactions and improved customer support.

---

## 🎯 Problem Statement

Traditional IVR systems face several limitations:

- Rigid **menu-driven navigation**
- Poor user experience during **high call volumes**
- Limited **scalability and personalization**
- Heavy reliance on **human support agents**

This project addresses these by introducing a **hybrid IVR architecture** powered by conversational AI.

---

## 🏗️ System Architecture

### 🧱 Traditional Layer
- VoiceXML (VXML) scripts
- DTMF-based menu navigation
- PSTN / SIP telephony infrastructure

### ⚙️ Modernization Layer
- Conversational AI with Natural Language Understanding (NLU)
- Intent detection and entity extraction
- Context-aware multi-turn conversation management

### ☁️ Cloud & Integration Layer
- Azure Communication Services (ACS) / Twilio
- Bot Application Platform (BAP)
- Backend service APIs (IRCTC systems)

---

## 📂 Repository Structure

```
├── milestone_2/                  # Integration Layer (FastAPI backend + Web Simulator)
│   ├── backend.py                # FastAPI middleware — IVR REST API
│   ├── ui.html                   # Web IVR Simulator UI
│   ├── requirements.txt          # Python dependencies
│   └── README_M2.md
│
├── milestone_3/                  # Conversational AI (Frontend-Only)
│   ├── irctc_conversational_ivr_m3.html   # Full NLU + STT + TTS simulator
│   └── README_M3.md
│
├── milestone_4/                  # Testing Suite
│   ├── tests/
│   │   ├── test_unit.py          # Unit tests — isolated route handlers
│   │   ├── test_integration.py   # Integration tests — session state machine
│   │   ├── test_e2e.py           # End-to-end full call journey tests
│   │   ├── test_performance.py   # Load tests — P95, throughput, error rate
│   │   └── test_error_handling.py # Error handling + structured logging
│   ├── pytest.ini
│   └── requirements-test.txt
│
├── MIT license.txt
└── README.md
```

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|-----------|--------|-------------|
| M1 | ✅ Done | Legacy system analysis & requirements |
| M2 | ✅ Done | FastAPI integration layer + Web IVR Simulator |
| M3 | ✅ Done | Conversational AI — NLU, STT, TTS (browser-native) |
| M4 | ✅ Done | Testing suite + Vercel deployment |

---

## 🚀 Milestone 2 — Integration Layer

A **FastAPI-based middleware** that connects legacy VXML IVR systems with modern conversational AI platforms.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ivr/start` | Start IVR session — welcome prompt |
| `POST` | `/ivr/input` | DTMF key press handler |
| `POST` | `/ivr/pnr` | PNR status check |
| `POST` | `/ivr/booking` | Smart ticket booking |
| `POST` | `/ivr/tatkal` | Tatkal emergency booking |
| `POST` | `/ivr/tracking` | Live train tracking |
| `POST` | `/acs/bridge` | ACS/BAP connector bridge |
| `GET`  | `/session/{id}` | Get session state |
| `GET`  | `/health` | Health check |

### Run Locally

```bash
pip install -r milestone_2/requirements.txt
python milestone_2/backend.py
# Open http://localhost:8000
```

---

## 🤖 Milestone 3 — Conversational AI Simulator

A **zero-backend, browser-native** conversational IVR simulator with full NLU pipeline.

**Tech:** HTML5 · Vanilla JS · Web Speech API (STT) · SpeechSynthesis (TTS)

**NLU Pipeline (all client-side):**
- Intent detection via regex pattern scoring (9 intents)
- Entity extraction — stations, PNR, dates, travel class, train numbers
- Finite state machine dialogue manager with multi-turn context

**Supported Intents:** Book Ticket · PNR Status · Train Schedule · Cancel Ticket · Fare Enquiry · Running Status · Complaint

### Run Locally

```bash
python -m http.server 5500
# Open http://localhost:5500/milestone_3/irctc_conversational_ivr_m3.html
# Requires Chrome or Edge for Web Speech API
```

---

## 🧪 Milestone 4 — Testing & Deployment

### Test Suite (108 tests, all passing)

| File | Type | Tests | What it covers |
|------|------|-------|----------------|
| `test_unit.py` | Unit | 50 | Every endpoint in isolation — 200s, 422s, 404s, response shapes |
| `test_integration.py` | Integration | 21 | Session persistence, state transitions, booking slot accumulation |
| `test_e2e.py` | End-to-End | 11 | Full user journeys — PNR, booking, tracking, Tatkal, agent transfer |
| `test_performance.py` | Performance | 10 | 50 concurrent requests, P95 < 500ms, avg < 200ms, ≥10 req/s |
| `test_error_handling.py` | Error Handling | 30 | 404s, 422s, business logic errors, structured logging |

### Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| Average response time | < 200ms | ✅ |
| P95 response time | < 500ms | ✅ |
| Error rate (expected load) | 0% | ✅ |
| Throughput | ≥ 10 req/s | ✅ |

### Run Tests

```bash
pip install -r milestone_2/requirements.txt
pip install -r milestone_4/requirements-test.txt

# All tests
python -m pytest milestone_4/tests/ -v

# By type
python -m pytest milestone_4/tests/test_unit.py -v
python -m pytest milestone_4/tests/test_integration.py -v
python -m pytest milestone_4/tests/test_e2e.py -v
python -m pytest milestone_4/tests/test_performance.py -v -s
python -m pytest milestone_4/tests/test_error_handling.py -v

# With coverage
python -m pytest milestone_4/tests/test_unit.py --cov=milestone_2/backend --cov-report=term-missing
```

### Deployment — Vercel

The project is deployed on Vercel at:
**[https://ai-enabled-conversational-ivr-moder.vercel.app/](https://ai-enabled-conversational-ivr-moder.vercel.app/)**

To redeploy:
```bash
npm i -g vercel
vercel --prod
```

---

## 🛠️ Technologies Used

| Layer | Technologies |
|-------|-------------|
| Backend | FastAPI, Uvicorn, Pydantic, Python 3.11 |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Poppins / Fira Code |
| NLU | Regex pattern matching, Finite state machine (client-side JS) |
| Speech | Web Speech API (STT), SpeechSynthesis API (TTS) |
| Telephony | Azure Communication Services (ACS), Twilio (stub) |
| Testing | pytest, pytest-cov, FastAPI TestClient |
| Deployment | Vercel |

---

## 📌 How to Use This Repository

- 📘 Understand the differences between traditional and modern IVR systems
- 🧠 Explore IVR modernization strategies with conversational AI
- 🏗️ Build similar systems for telecom, banking, or government platforms
- 🎓 Use as a reference for academic projects, internships, or research
