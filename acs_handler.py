from fastapi import APIRouter, Request, BackgroundTasks
from azure.communication.callautomation import (
    CallAutomationClient,
    PhoneNumberIdentifier,
    TextSource,
    RecognizeInputType
)
import os
import logging
from typing import Dict, Any

from session_manager import session_manager
from middleware import process_user_input

router = APIRouter(prefix="/acs", tags=["ACS Call Handling"])
logger = logging.getLogger("acs_handler")

# Assuming ACS is configured via environment variables
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING", "endpoint=https://sample.communication.azure.com/;accesskey=sample")
CALLBACK_URI = os.getenv("CALLBACK_URI", "http://localhost:8000/acs/callbacks")

# Initialize CallAutomationClient - handle failure gracefully for local mock-only testing
try:
    call_automation_client = CallAutomationClient.from_connection_string(ACS_CONNECTION_STRING)
    logger.info("CallAutomationClient initialized successfully.")
except ValueError:
    call_automation_client = None
    logger.warning("CallAutomationClient skipped. Connection string invalid or missing. Will mock call actions.")

@router.post("/incoming-call")
async def incoming_call(request: Request):
    """
    Handle Event Grid / Webhook events from ACS for incoming calls.
    """
    events = await request.json()
    for event in events:
        # Step 1: Handle EventGrid Subscription Validation
        if event.get("eventType") == "Microsoft.EventGrid.SubscriptionValidationEvent":
            validation_code = event["data"]["validationCode"]
            logger.info("Validated EventGrid Subscription")
            return {"validationResponse": validation_code}
        
        # Step 2: Handle Incoming Call Event
        if event.get("eventType") == "Microsoft.Communication.IncomingCall":
            incoming_call_context = event["data"]["incomingCallContext"]
            caller_id = event["data"]["from"]["rawId"]
            
            logger.info(f"Incoming call received from {caller_id}")
            
            # Answer the call via ACS SDK using the event-driven context
            if call_automation_client:
                try:
                    answer_call_result = call_automation_client.answer_call(
                        incoming_call_context=incoming_call_context,
                        callback_url=CALLBACK_URI
                    )
                    logger.info(f"Answered call. Connection ID: {answer_call_result.call_connection_id}")
                except Exception as e:
                    logger.error(f"Failed to answer call via SDK: {e}")
            else:
                logger.warning("Mocking answer. CallAutomationClient not available.")
                
            return {"status": "Incoming call answered"}
            
    return {"status": "ok"}

@router.post("/callbacks")
async def acs_callbacks(request: Request, background_tasks: BackgroundTasks):
    """
    Handle mid-call events (CallConnected, RecognizeCompleted, etc.)
    Follows CloudEvents schema as defined by ACS SDK callbacks.
    """
    events = await request.json()
    # It might be a single dict or a list depending on ACS schema payload
    if isinstance(events, dict):
        events = [events]

    for event in events:
        event_type = event.get("type", "")
        event_data = event.get("data", {})
        call_connection_id = event_data.get("callConnectionId")
        
        if not call_connection_id:
            continue

        logger.info(f"Received ACS Event: {event_type} for call {call_connection_id}")
        
        if event_type == "Microsoft.Communication.CallConnected":
            # Initialize a new session
            caller_raw_id = "unknown" # Can be extracted from earlier context or call props
            session_manager.create_session(call_connection_id, caller_raw_id)
            
            logger.info("Call connected. Playing welcome prompt and starting recognition.")
            
            # Start continuous recognition
            if call_automation_client:
                try:
                    call_connection_client = call_automation_client.get_call_connection(call_connection_id)
                    play_source = TextSource(text="Welcome to the Conversational Railway System. How can I help you? You can ask about PNR status, Train Running Status, or Book a Ticket. Or press 1 for PNR Status.")
                    
                    # Begin multi-modal recognition (speech + DTMF)
                    call_connection_client.start_recognizing_media(
                        input_type=RecognizeInputType.SPEECH_OR_DTMF, # Assume choices, or speech, custom SDK enums applied
                        target_participant=PhoneNumberIdentifier(caller_raw_id) if caller_raw_id != "unknown" else None, # Real apps need actual participant object
                        play_prompt=play_source,
                        interrupt_prompt=True,
                        initial_silence_timeout=10,
                        dtmf_max_tones_to_collect=10,
                        dtmf_inter_tone_timeout=5
                    )
                except Exception as e:
                    logger.error(f"Failed to start recognition: {e}")
            
        elif event_type == "Microsoft.Communication.RecognizeCompleted":
            # Extract recognized text or DTMF
            recognition_type = event_data.get("recognitionType")
            text = None
            dtmf = None
            
            if recognition_type == "speech":
                text = event_data.get("speechResult", {}).get("text")
                logger.info(f"Recognized Speech: {text}")
            elif recognition_type == "dtmf":
                tones = event_data.get("dtmfResult", {}).get("tones", [])
                # The tone enumeration usually has values like "one", "two".
                # For simplicity in mock, assume we map it down to standard digits.
                dtmf_mapping = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "zero": "0", "star": "*", "pound": "#"}
                mapped_tones = [dtmf_mapping.get(t, t) for t in tones]
                dtmf = "".join(mapped_tones)
                logger.info(f"Recognized DTMF: {dtmf}")
                
            # Process in background task to avoid blocking the ACS callback acknowledgment loop
            background_tasks.add_task(handle_recognition, call_connection_id, text, dtmf)
            
        elif event_type == "Microsoft.Communication.RecognizeFailed":
            logger.warning(f"Recognition failed for call {call_connection_id}. Repeating prompt.")
            # Usually we check the error payload and trigger repeat prompt logic via start_recognizing_media
            # Omitted complex retry state here for brevity
            
        elif event_type == "Microsoft.Communication.CallDisconnected":
            logger.info(f"Call {call_connection_id} disconnected. Cleaning up session.")
            session_manager.delete_session(call_connection_id)
            
    return {"status": "received"}

async def handle_recognition(call_id: str, text: str, dtmf: str):
    """
    Background worker that hits the middleware, processes AI rules,
    and instructs ACS to play the response.
    """
    response_text = await process_user_input(call_id, text, dtmf)
    logger.info(f"Middleware generated response for ACS: {response_text}")
    
    if call_automation_client:
        try:
            call_connection_client = call_automation_client.get_call_connection(call_id)
            play_source = TextSource(text=response_text)
            
            session = session_manager.get_session(call_id)
            
            if session and session.conversation_state == "COMPLETED":
                # Final response and hang up
                # Or just play to all and disconnect
                logger.info("Conversation COMPLETED. Playing final message.")
                # Could be a play_to_all and then await PlayCompleted event to disconnect
            else:
                # Continue interacting
                call_connection_client.start_recognizing_media(
                    input_type=RecognizeInputType.SPEECH_OR_DTMF,
                    target_participant=None,
                    play_prompt=play_source,
                    interrupt_prompt=True,
                    dtmf_max_tones_to_collect=10
                )
        except Exception as e:
            logger.error(f"Failed to play back response to ACS: {e}")
