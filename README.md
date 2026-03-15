<<<<<<< HEAD
# IRCTC Modern IVR System

A modern, sleek UI implementation of the IRCTC Smart IVR Integration Layer with all the same features as the original project.

## Features

✅ All features from the original IRCTC IVR project:
- PNR Status Check
- Smart Ticket Booking (with class, quota, and berth preferences)
- Tatkal Emergency Booking
- Live Train Tracking
- Cancel & Refund
- Agent Transfer
- Session Management
- Activity Logging
- Real-time API Response Viewer

## Tech Stack

- **Backend**: FastAPI (Python)
- **Server**: Uvicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Fonts**: Inter, JetBrains Mono

## Installation

1. Navigate to the project folder:
```bash
cd irctc_modern
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
python backend.py
```

The server will start on `http://localhost:8000`

Open your browser and navigate to:
```
http://localhost:8000
```

## How to Use

1. **Start Call**: Click the "START CALL" button to initiate an IVR session
2. **Use Dialpad**: Press keys 1-5 to navigate different services
3. **Quick Services**: Click on service cards for direct API calls
4. **View Responses**: See real-time JSON responses in the API Response panel
5. **Monitor Activity**: Track all interactions in the Activity Log
6. **End Call**: Click "END CALL" to terminate the session

## UI Differences from Original

This version features a completely redesigned modern UI with:
- Gradient backgrounds and glassmorphism effects
- Smooth animations and transitions
- Modern color scheme (dark blue/purple theme)
- Enhanced typography with Inter and JetBrains Mono fonts
- Improved visual hierarchy
- Better responsive design
- Sleeker card-based layout

## API Endpoints

Same as the original project:
- `POST /ivr/start` - Start IVR session
- `POST /ivr/input` - Handle DTMF input
- `POST /ivr/pnr` - Check PNR status
- `POST /ivr/booking` - Smart ticket booking
- `POST /ivr/tatkal` - Tatkal emergency booking
- `POST /ivr/tracking` - Live train tracking
- `POST /acs/bridge` - ACS/BAP connector
- `GET /session/{session_id}` - Get session state
- `GET /health` - Health check

## Project Structure

```
irctc_modern/
├── backend.py          # FastAPI backend (same functionality)
├── ui.html            # Modern UI (completely redesigned)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Notes

- All backend functionality is identical to the original project
- Only the UI/UX has been completely redesigned
- Same tech stack maintained (FastAPI + HTML/CSS/JS)
- All features work exactly the same way
=======
# 📞 Conversational IVR Modernization Framework

### IRCTC-Focused Hybrid IVR using ACS & BAP

## 🧩 Project Overview

This project aims to modernize the traditional **IRCTC Interactive Voice
Response (IVR)** system by integrating cloud-based conversational AI
technologies. The objective is to enhance the existing IVR
infrastructure while preserving its legacy logic.

Instead of replacing the entire system, this approach extends the
current **VoiceXML-based IVR** with intelligent conversational
capabilities. By incorporating modern communication platforms and AI
services, the system becomes more scalable, flexible, and user-friendly.

The framework demonstrates how legacy IVR systems can be integrated with
modern services such as **Azure Communication Services (ACS)**,
**Twilio**, and **Bot Application Platforms (BAP)** to enable natural
language interactions and improved customer support.

The IRCTC IVR system serves as the primary case study in this project
because it operates at a **national scale** and supports a large,
diverse user base. The framework illustrates how similar large-scale
systems can be upgraded without rebuilding the entire infrastructure.

------------------------------------------------------------------------

## 🎯 Problem Statement

Many traditional IVR systems used by large service platforms face
several limitations, including:

-   Rigid **menu-driven navigation**
-   Poor user experience during **high call volumes**
-   Limited **scalability and personalization**
-   Heavy reliance on **human support agents**

This project addresses these issues by introducing a **hybrid IVR
architecture** powered by conversational AI.

------------------------------------------------------------------------

## 🏗️ System Architecture (High-Level)

### 🧱 Traditional Layer

-   VoiceXML (VXML) scripts\
-   DTMF-based menu navigation\
-   PSTN / SIP telephony infrastructure

### ⚙️ Modernization Layer

-   Conversational AI with Natural Language Understanding (NLU)\
-   Intent detection and processing\
-   Context-aware conversation management

### ☁️ Cloud & Integration Layer

-   Azure Communication Services (ACS) or Twilio\
-   Bot Application Platform (BAP)\
-   Backend service APIs (IRCTC systems)

------------------------------------------------------------------------

## 🔄 Implementation Workflow

1.  📞 A user calls the **IRCTC IVR phone number**\
2.  🎧 The call is received through **ACS or Twilio**\
3.  🤖 User input is captured via **voice or keypad (DTMF)**\
4.  🧠 An NLP engine analyzes the request and detects the **user
    intent**\
5.  🔁 Relevant **IRCTC backend services** are invoked\
6.  🗣️ The response is converted to **speech output**\
7.  📲 The call continues with automated assistance or is **escalated to
    a human agent**

This hybrid architecture ensures **compatibility with legacy IVR systems
while enabling modern conversational capabilities**.

------------------------------------------------------------------------

## 🛠️ Technologies Used

-   **VoiceXML (VXML)**
-   **Azure Communication Services (ACS)** / **Twilio**
-   **Bot Application Platform (BAP)**
-   **REST APIs**
-   **Natural Language Processing (NLP) & Intent Recognition**
-   **Cloud Infrastructure**

------------------------------------------------------------------------

## 📂 Repository Purpose

This repository provides:

-   Analysis of traditional IVR system architecture\
-   A strategy for **modernizing legacy IVR platforms**\
-   An **IRCTC-focused implementation model**\
-   Considerations for **scalability, integration, and security**

The repository serves as a **reference framework for upgrading existing
IVR systems using conversational AI technologies**.

------------------------------------------------------------------------

## 📌 How to Use This Repository

You can use this repository to:

-   📘 Understand the differences between **traditional and modern IVR
    systems**
-   🧠 Explore **IVR modernization strategies**
-   🏗️ Build similar systems for **telecom, banking, or government
    service platforms**
-   🎓 Use it as a **reference for academic projects, internships, or
    research work**
>>>>>>> 87d03c3 (milestone_3)
