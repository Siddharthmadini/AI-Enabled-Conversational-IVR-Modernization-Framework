## IRCTC Conversational IVR — Milestone 3

Minimal front‑end simulator of an IRCTC style IVR with:
- text and optional voice input
- basic intent and entity detection
- DTMF keypad
- a small debug panel to inspect state.

### Files

- `irctc_conversational_ivr_m3.html` – original milestone 3 UI
- `irctc_conversational_ivr_m3_v2.html` – redesigned UI with the same behaviour
- `README_M3.md` – this file

### How to run

1. Start any simple web server in this folder (for example, using VS Code Live Server or `python -m http.server`).
2. Open `irctc_conversational_ivr_m3_v2.html` in Chrome or Edge.
3. Allow microphone access if you want to test speech; otherwise you can use text and the DTMF keypad.

All logic runs entirely in the browser; there is no backend required for this milestone.
