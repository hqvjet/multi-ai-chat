from pydantic import BaseModel
from typing import List

class ChatResponse(BaseModel):
    response: str

# conversation required
class ChatRequest(BaseModel):
    role: str
    message: List[List[str]]

class ConversationHistory(BaseModel):
    conversation_history: List[ChatRequest]

class TokenRemaining(BaseModel):
    token_remaining: int
