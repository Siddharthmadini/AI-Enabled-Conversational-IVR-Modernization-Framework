import logging
from typing import Optional
from session_manager import session_manager
import httpx
import os

logger = logging.getLogger("middleware")

AI_THRESHOLD = 0.75
# For testing locally, assuming AI and IRCTC mocks are on the same host/port
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

async def process_user_input(call_id: str, text: Optional[str] = None, dtmf: Optional[str] = None) -> str:
    """
    Process incoming user input (text or DTMF), coordinate with AI, update session, and determine next action.
    """
    session = session_manager.get_session(call_id)
    if not session:
        logger.error(f"Session not found for call {call_id}")
        return "Your session has expired. Please call again."

    logger.info(f"Processing input for {call_id}: text='{text}', dtmf='{dtmf}'")

    if dtmf:
        return await process_dtmf(session, dtmf)
    
    if not text:
        return "I didn't catch that. Could you please repeat?"

    # Call AI mock to detect intent and entities
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{BASE_URL}/ai/detect-intent", json={"text": text})
            resp.raise_for_status()
            ai_data = resp.json()
        except Exception as e:
            logger.error(f"AI API failed: {e}")
            return "Sorry, our AI service is currently down. Please try again later."

    intent = ai_data.get("intent", "unknown")
    confidence = ai_data.get("confidence", 0.0)
    entities = ai_data.get("entities", {})

    logger.info(f"AI Response - Intent: {intent}, Confidence: {confidence}, Entities: {entities}")

    if confidence < AI_THRESHOLD:
        logger.warning(f"Confidence {confidence} below threshold {AI_THRESHOLD}. Triggering fallback.")
        return execute_fallback(session)

    # Update session with new intent & entities
    if session.current_intent is None or intent != "unknown":
        session.current_intent = intent
    
    session.collected_slots.update(entities)
    session_manager.update_session(call_id, {
        "current_intent": session.current_intent,
        "collected_slots": session.collected_slots
    })

    # Execute business logic based on determined intent
    return await execute_intent_logic(session)


async def process_dtmf(session, dtmf: str) -> str:
    """
    Hybrid fallback/DTMF support. Example flows for DTMF menus.
    """
    logger.info(f"Processing DTMF for state: {session.conversation_state}, input: {dtmf}")
    
    if session.conversation_state == "INIT":
        if dtmf == "1":
            session.current_intent = "reservation_status"
            session.conversation_state = "COLLECTING_PNR"
            session_manager.update_session(session.call_id, {
                "current_intent": "reservation_status",
                "conversation_state": "COLLECTING_PNR"
            })
            return "You have selected Reservation Status. Please enter your 10 digit PNR."
        elif dtmf == "2":
            session.current_intent = "train_running_status"
            session.conversation_state = "COLLECTING_TRAIN_NUM"
            session_manager.update_session(session.call_id, {
                "current_intent": "train_running_status",
                "conversation_state": "COLLECTING_TRAIN_NUM"
            })
            return "You have selected Train Running Status. Please enter your 5 digit train number."
    
    elif session.conversation_state == "COLLECTING_PNR":
        session.collected_slots["pnr"] = dtmf
        session_manager.update_session(session.call_id, {"collected_slots": session.collected_slots})
        return await execute_intent_logic(session)
        
    elif session.conversation_state == "COLLECTING_TRAIN_NUM":
        session.collected_slots["train_number"] = dtmf
        session_manager.update_session(session.call_id, {"collected_slots": session.collected_slots})
        return await execute_intent_logic(session)
        
    return "Invalid input or menu state. Please try again or say 'help'."


def execute_fallback(session) -> str:
    """
    Fallback logic for when AI confidence is too low.
    """
    logger.info(f"Fallback executed for {session.call_id}")
    # In a real scenario, this might transfer the call to a legacy VXML flow or human agent
    return "I am having trouble understanding. Please use your keypad. Press 1 for Reservation Status, or Press 2 for Train Running Status."


async def execute_intent_logic(session) -> str:
    """
    Route to appropriate IRCTC mock API depending on current intent and collected slots.
    """
    intent = session.current_intent
    slots = session.collected_slots

    if intent == "reservation_status":
        if "pnr" not in slots:
            session.conversation_state = "COLLECTING_PNR"
            session_manager.update_session(session.call_id, {"conversation_state": "COLLECTING_PNR"})
            return "Please tell me or enter your 10-digit PNR number."
        else:
            # Complete the slot filling, call backend IRCTC
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/irctc/reservation-status", json={"pnr": slots["pnr"]})
                if res.status_code == 200:
                    data = res.json()
                    status = data.get("status", "Unknown")
                    session.conversation_state = "COMPLETED"
                    session_manager.update_session(session.call_id, {"conversation_state": "COMPLETED"})
                    return f"Your reservation status for PNR {slots['pnr']} is {status}. Thank you for using IRCTC."
                return "Failed to fetch reservation status from IRCTC."
                
    elif intent == "train_running_status":
        if "train_number" not in slots:
            session.conversation_state = "COLLECTING_TRAIN_NUM"
            session_manager.update_session(session.call_id, {"conversation_state": "COLLECTING_TRAIN_NUM"})
            return "Please tell me or enter your 5-digit train number."
        else:
            async with httpx.AsyncClient() as client:
                res = await client.post(f"{BASE_URL}/irctc/train-running-status", json={"train_number": slots["train_number"]})
                if res.status_code == 200:
                    data = res.json()
                    status = data.get("status")
                    delay = data.get("delay_minutes", 0)
                    delay_msg = f"with a delay of {delay} minutes" if delay > 0 else "on time"
                    session.conversation_state = "COMPLETED"
                    session_manager.update_session(session.call_id, {"conversation_state": "COMPLETED"})
                    return f"Train {slots['train_number']} is currently {status} {delay_msg}. Current station is {data.get('current_station')}."
                return "Failed to fetch train status from IRCTC."
                
    elif intent == "book_ticket":
        return "Ticket booking requires multiple details. Where would you like to travel from?"
        
    elif intent == "train_availability":
        return "To check availability, please provide source, destination, and date."

    return "I understood your request but I am still learning how to handle it. You can ask me for your PNR status or train running status."
