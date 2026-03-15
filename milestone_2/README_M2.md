## IRCTC Smart IVR — Milestone 2 (Integration Layer)

Milestone 2 focuses on building a **FastAPI-based integration layer** with a simple **web IVR simulator**.  
It exposes REST APIs for IVR call flows (start call, DTMF input, PNR status, booking, etc.) and returns JSON responses that the UI renders.

---

## What Milestone 2 Delivers

- **FastAPI backend** for IVR-style endpoints  
  - `POST /ivr/start` — start a call and create a session  
  - `POST /ivr/input` — handle key presses (DTMF)  
  - `POST /ivr/pnr` — sample PNR status response  
  - `POST /ivr/booking` — sample smart booking response  
- **Static HTML UI** to simulate a phone dialpad and show JSON responses

---

## How to Run

**Prerequisite**

- Python 3.10+

**Install dependencies**

```bash
pip install fastapi uvicorn requests
```

**Start the backend**

```bash
python irctc_backend.py
```

**Open the simulator**

- Open `irctc_ui.html` in a browser, or  
- If served by FastAPI, open `http://localhost:8000`

**API docs (optional)**

- `http://localhost:8000/docs`

---

## Basic Usage Flow

1. Open the web IVR simulator in your browser.  
2. Click **START CALL** to create a session.  
3. Use the dialpad buttons (1–4) to navigate flows like PNR, booking, tatkal, or live tracking.  
4. View the JSON request/response for each action in the UI.  
5. Click **END CALL** to finish the session.

---

## Files in This Milestone

- `irctc_backend.py` — FastAPI integration layer  
- `irctc_ui.html` — web IVR simulator UI
