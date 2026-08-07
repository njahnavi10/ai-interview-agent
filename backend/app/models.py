from pydantic import BaseModel
from typing import Optional, Dict


class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[Dict] = None
    message: Optional[str] = None


class InterviewResponse(BaseModel):
    reply: str
    done: bool
    feedback: Optional[Dict] = None