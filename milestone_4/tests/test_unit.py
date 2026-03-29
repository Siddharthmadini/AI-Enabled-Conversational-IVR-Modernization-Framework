"""
=============================================================================
MODULE 4 — Unit Tests (Track C: Web Simulator)
Tests individual FastAPI route handlers in total isolation.
Each test runs against TestClient — no real server, no real network calls.
=============================================================================
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../milestone_2"))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend import app

client = TestClient(app)


# ── helpers ──────────────────────────────────────────────────────────────────

def start_session(caller_id="+919876543210"):
    """Convenience: start a call and return the session_id."""
    resp = client.post("/ivr/start", json={"caller_id": caller_id, "language": "EN"})
    assert resp.status_code == 200
    return resp.json()["data"]["session_id"]


# ── C1-1  Root / health endpoint ─────────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_returns_welcome_message(self):
        resp = client.get("/health")
        body = resp.json()
        assert body["status"] == "success"
        assert "IRCTC" in body["prompt"]

    def test_health_contains_version(self):
        resp = client.get("/health")
        assert resp.json()["data"]["version"] == "2.0.0"

    def test_health_lists_endpoints(self):
        resp = client.get("/health")
        endpoints = resp.json()["data"]["endpoints"]
        assert "/ivr/start" in endpoints
        assert "/ivr/pnr" in endpoints


# ── C1-2  /ivr/start ─────────────────────────────────────────────────────────

class TestIVRStart:
    def test_start_returns_200(self):
        resp = client.post("/ivr/start", json={"caller_id": "+911234567890"})
        assert resp.status_code == 200

    def test_start_returns_session_id(self):
        resp = client.post("/ivr/start", json={"caller_id": "+911234567890"})
        data = resp.json()["data"]
        assert "session_id" in data
        assert len(data["session_id"]) > 0

    def test_start_returns_menu(self):
        resp = client.post("/ivr/start", json={"caller_id": "+911234567890"})
        menu = resp.json()["data"]["menu"]
        assert "1" in menu   # PNR
        assert "2" in menu   # Booking
        assert "9" in menu   # Agent

    def test_start_prompt_contains_welcome(self):
        resp = client.post("/ivr/start", json={"caller_id": "+911234567890"})
        assert "Welcome" in resp.json()["prompt"]

    def test_start_missing_caller_id_returns_422(self):
        resp = client.post("/ivr/start", json={"language": "EN"})
        assert resp.status_code == 422

    def test_start_empty_body_returns_422(self):
        resp = client.post("/ivr/start", json={})
        assert resp.status_code == 422

    def test_start_acs_connection_id_optional(self):
        resp = client.post("/ivr/start", json={
            "caller_id": "+911234567890",
            "acs_call_connection_id": "acs-conn-abc123"
        })
        assert resp.status_code == 200


# ── C1-3  /ivr/input (DTMF) ──────────────────────────────────────────────────

class TestDTMFInput:
    def test_valid_digit_1_routes_to_pnr(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "main_menu"
        })
        assert resp.status_code == 200
        assert resp.json()["acs_event"] == "pnr_flow"

    def test_valid_digit_2_routes_to_booking(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "2", "current_flow": "main_menu"
        })
        assert resp.json()["acs_event"] == "booking_flow"

    def test_valid_digit_9_transfers_to_agent(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "9", "current_flow": "main_menu"
        })
        assert resp.json()["acs_event"] == "agent_transfer"
        assert resp.json()["status"] == "transfer"

    def test_invalid_digit_returns_invalid_status(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "8", "current_flow": "main_menu"
        })
        assert resp.json()["status"] == "invalid"

    def test_digit_0_repeats_menu(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "0", "current_flow": "main_menu"
        })
        assert resp.json()["acs_event"] == "repeat_menu"

    def test_booking_class_selection(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_class"
        })
        assert resp.status_code == 200
        assert "Sleeper" in resp.json()["prompt"]

    def test_invalid_class_selection(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "9", "current_flow": "select_class"
        })
        assert resp.json()["status"] == "invalid"

    def test_quota_selection(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_quota"
        })
        assert "General" in resp.json()["prompt"]

    def test_berth_selection(self):
        sid = start_session()
        resp = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_berth"
        })
        assert "Lower" in resp.json()["prompt"]

    def test_unknown_session_returns_404(self):
        resp = client.post("/ivr/input", json={
            "session_id": "nonexistent-session", "digit": "1", "current_flow": "main_menu"
        })
        assert resp.status_code == 404

    def test_missing_session_id_returns_422(self):
        resp = client.post("/ivr/input", json={"digit": "1", "current_flow": "main_menu"})
        assert resp.status_code == 422


# ── C1-4  /ivr/pnr ───────────────────────────────────────────────────────────

class TestPNRCheck:
    def test_valid_pnr_returns_confirmed(self):
        sid = start_session()
        resp = client.post("/ivr/pnr", json={"session_id": sid, "pnr_number": "4521679834"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"
        assert "CONFIRMED" in resp.json()["prompt"]

    def test_pnr_response_contains_train_info(self):
        sid = start_session()
        resp = client.post("/ivr/pnr", json={"session_id": sid, "pnr_number": "4521679834"})
        data = resp.json()["data"]["pnr_details"]
        assert "train" in data
        assert "coach" in data
        assert "berth" in data

    def test_invalid_pnr_too_short(self):
        sid = start_session()
        resp = client.post("/ivr/pnr", json={"session_id": sid, "pnr_number": "12345"})
        assert resp.json()["status"] == "invalid"

    def test_invalid_pnr_non_numeric(self):
        sid = start_session()
        resp = client.post("/ivr/pnr", json={"session_id": sid, "pnr_number": "ABCD123456"})
        assert resp.json()["status"] == "invalid"

    def test_pnr_missing_session_returns_422(self):
        resp = client.post("/ivr/pnr", json={"pnr_number": "4521679834"})
        assert resp.status_code == 422


# ── C1-5  /ivr/booking ───────────────────────────────────────────────────────

class TestSmartBooking:
    VALID_BOOKING = {
        "train_number": "12951",
        "journey_date": "15032026",
        "from_station": "NDLS",
        "to_station": "MMCT",
        "travel_class": "2",
        "quota": "1",
        "berth_preference": "1",
        "passenger_count": 1,
    }

    def test_valid_booking_returns_201_equivalent(self):
        sid = start_session()
        resp = client.post("/ivr/booking", json={"session_id": sid, **self.VALID_BOOKING})
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_booking_returns_booking_id(self):
        sid = start_session()
        resp = client.post("/ivr/booking", json={"session_id": sid, **self.VALID_BOOKING})
        booking = resp.json()["data"]["booking"]
        assert "booking_id" in booking
        assert booking["booking_id"].startswith("BK")

    def test_booking_id_echoed_in_response(self):
        sid = start_session()
        resp = client.post("/ivr/booking", json={"session_id": sid, **self.VALID_BOOKING})
        bid = resp.json()["data"]["booking"]["booking_id"]
        assert bid in resp.json()["prompt"]

    def test_booking_fare_calculated(self):
        sid = start_session()
        resp = client.post("/ivr/booking", json={"session_id": sid, **self.VALID_BOOKING})
        fare = resp.json()["data"]["booking"]["fare"]
        assert "₹" in fare

    def test_booking_missing_train_number_returns_422(self):
        sid = start_session()
        payload = {k: v for k, v in self.VALID_BOOKING.items() if k != "train_number"}
        resp = client.post("/ivr/booking", json={"session_id": sid, **payload})
        assert resp.status_code == 422

    def test_booking_missing_session_returns_422(self):
        resp = client.post("/ivr/booking", json=self.VALID_BOOKING)
        assert resp.status_code == 422


# ── C1-6  /ivr/tatkal ────────────────────────────────────────────────────────

class TestTatkalBooking:
    VALID_TATKAL = {
        "train_number": "12951",
        "journey_date": "15032026",
        "from_station": "NDLS",
        "to_station": "MMCT",
        "travel_class": "2",
        "passenger_count": 1,
    }

    def test_tatkal_returns_ref_id(self):
        sid = start_session()
        resp = client.post("/ivr/tatkal", json={"session_id": sid, **self.VALID_TATKAL})
        # Either queued or closed depending on time — both are valid responses
        assert resp.status_code == 200

    def test_tatkal_queued_contains_surcharge(self):
        sid = start_session()
        resp = client.post("/ivr/tatkal", json={"session_id": sid, **self.VALID_TATKAL})
        body = resp.json()
        # If window is open, check surcharge; if closed, check message
        if body["status"] == "success":
            assert "surcharge" in body["data"]["tatkal"]
        else:
            assert body["status"] == "unavailable"

    def test_tatkal_missing_session_returns_422(self):
        resp = client.post("/ivr/tatkal", json=self.VALID_TATKAL)
        assert resp.status_code == 422


# ── C1-7  /ivr/tracking ──────────────────────────────────────────────────────

class TestLiveTracking:
    def test_valid_train_returns_tracking_data(self):
        sid = start_session()
        resp = client.post("/ivr/tracking", json={"session_id": sid, "train_number": "12951"})
        assert resp.status_code == 200
        assert "tracking" in resp.json()["data"]

    def test_tracking_contains_station_info(self):
        sid = start_session()
        resp = client.post("/ivr/tracking", json={"session_id": sid, "train_number": "12951"})
        track = resp.json()["data"]["tracking"]
        assert "current_station" in track
        assert "next_station" in track
        assert "delay_minutes" in track

    def test_invalid_train_number_too_short(self):
        sid = start_session()
        resp = client.post("/ivr/tracking", json={"session_id": sid, "train_number": "123"})
        assert resp.json()["status"] == "invalid"

    def test_non_numeric_train_number(self):
        sid = start_session()
        resp = client.post("/ivr/tracking", json={"session_id": sid, "train_number": "ABCDE"})
        assert resp.json()["status"] == "invalid"

    def test_tracking_missing_session_returns_422(self):
        resp = client.post("/ivr/tracking", json={"train_number": "12951"})
        assert resp.status_code == 422


# ── C1-8  /acs/bridge ────────────────────────────────────────────────────────

class TestACSBridge:
    def test_bridge_filled_event(self):
        sid = start_session()
        resp = client.post("/acs/bridge", json={
            "session_id": sid,
            "acs_call_connection_id": "conn-abc",
            "vxml_event": "filled",
        })
        assert resp.status_code == 200
        assert resp.json()["acs_event"] == "USER_INPUT_RECEIVED"

    def test_bridge_disconnect_event(self):
        sid = start_session()
        resp = client.post("/acs/bridge", json={
            "session_id": sid,
            "acs_call_connection_id": "conn-abc",
            "vxml_event": "disconnect",
        })
        assert resp.json()["acs_event"] == "END_SESSION"

    def test_bridge_unknown_event_returns_unknown(self):
        sid = start_session()
        resp = client.post("/acs/bridge", json={
            "session_id": sid,
            "acs_call_connection_id": "conn-abc",
            "vxml_event": "something_random",
        })
        assert resp.json()["acs_event"] == "UNKNOWN"


# ── C1-9  /session/{id} ──────────────────────────────────────────────────────

class TestSessionEndpoint:
    def test_get_existing_session(self):
        sid = start_session()
        resp = client.get(f"/session/{sid}")
        assert resp.status_code == 200
        assert resp.json()["data"]["session_id"] == sid

    def test_get_nonexistent_session_returns_404(self):
        resp = client.get("/session/does-not-exist")
        assert resp.status_code == 404
