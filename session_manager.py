from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class SessionState(BaseModel):
    call_id: str
    caller_number: str
    current_intent: Optional[str] = None
    collected_slots: Dict[str, Any] = Field(default_factory=dict)
    conversation_state: str = "INIT"
    start_time: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class SessionManager:
    def __init__(self):
        # In-memory dictionary for session management mapping call_id to SessionState
        self.sessions: Dict[str, SessionState] = {}

    def create_session(self, call_id: str, caller_number: str) -> SessionState:
        session = SessionState(call_id=call_id, caller_number=caller_number)
        self.sessions[call_id] = session
        return session

    def get_session(self, call_id: str) -> Optional[SessionState]:
        return self.sessions.get(call_id)

    def update_session(self, call_id: str, updates: Dict[str, Any]):
        session = self.get_session(call_id)
        if session:
            for key, value in updates.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            self.sessions[call_id] = session

    def delete_session(self, call_id: str):
        if call_id in self.sessions:
            del self.sessions[call_id]

# Singleton instance for the application
session_manager = SessionManager()
