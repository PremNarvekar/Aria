from datetime import datetime, timezone
from typing import Any
from uuid import uuid4 

_research_sessions: dict[str, dict [str, Any]] = {}

def create_research_session(
    question: str,
    
) -> dict[str , Any]:
    research_id = str(uuid4())
    
    
    session = {
        "research_id": research_id,
        "question":question,
        "status":"queued",
        "create_at":datetime.now(timezone.utc).isoformat(),
        "update_at":datetime.now(timezone.utc).isoformat(),
        "report":None,
        "source":[],
        "error":None
    }
    
    _research_sessions[research_id] = session
    
    return session

def get_research_session(
    research_id:str,
    
) -> dict[str, Any] | None:
    
    return _research_sessions.get(research_id)

def update_research_session(
    research_id:str,
    **updates: Any
) -> dict[str, Any] | None:
    
    session = _research_session.get(research_id)
    
    if session is None:
        return None 
    
    session.update(updates)
    
    session['updated_at'] = (
        datetime.now(timezone.utc).isoformat()
    )
    
    return session 