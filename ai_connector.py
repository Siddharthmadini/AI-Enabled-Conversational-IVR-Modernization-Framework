from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger("ai_connector")

router = APIRouter(prefix="/ai", tags=["AI Connector"])

class AIRequest(BaseModel):
    text: str

class AIResponse(BaseModel):
    intent: str
    entities: Dict[str, Any]
    confidence: float

@router.post("/detect-intent", response_model=AIResponse)
async def detect_intent(req: AIRequest):
    """
    Mock endpoint to detect intent from text.
    Simulates the BAP AI Platform behavior.
    """
    text = req.text.lower()
    
    intent = "unknown"
    entities = {}
    confidence = 0.5
    
    # Simple keyword-based intent resolution for testing purposes
    if "pnr" in text or "status" in text and "reservation" in text:
        intent = "reservation_status"
        # Extract 10-digit number as PNR
        parts = text.split()
        for p in parts:
            if p.isdigit() and len(p) >= 8:
                entities["pnr"] = p
        confidence = 0.87
        
    elif "book" in text or "ticket" in text:
        intent = "book_ticket"
        confidence = 0.90
        
    elif "running" in text or "train status" in text:
        intent = "train_running_status"
        # Dummy Train Number extraction
        parts = text.split()
        for p in parts:
            if p.isdigit() and len(p) == 5:
                entities["train_number"] = p
        confidence = 0.85
        
    elif "availability" in text or "seats" in text:
        intent = "train_availability"
        confidence = 0.88
        
    logger.info(f"AI Mock Engine detected intent={intent} with {confidence} confidence for text='{text}'")    
        
    return AIResponse(intent=intent, entities=entities, confidence=confidence)
