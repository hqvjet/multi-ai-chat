from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str

class ChatRequest(BaseModel):
    message: str

class TokenRemaining(BaseModel):
    token_remaining: int
