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
