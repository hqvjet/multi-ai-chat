import fastapi
import asyncio
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import ChatRequest, ChatResponse, ConversationHistory, TokenResponse
from chat_platform.token_manager import TokenManager
from chat_platform.model_provider import ask


app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

token_manager = TokenManager()

def normalize_conversations(conversations: List[ChatRequest]) -> List[dict]:
    return [{"role": c.role, "content": ''.join([''.join(char) for char in c.message])} for c in conversations]

@app.put("/api/v1/update_token", response_model=TokenResponse)
async def update_token(req: ConversationHistory, res: ChatResponse):
    token_manager.update_token_remaining(req.conversation_history, res.response)

    return TokenResponse(token_remaining=token_manager.get_token_remaining(), model_name=token_manager.get_model_name())

@app.get("/api/v1/token", response_model=TokenResponse)
async def get_token():
    return TokenResponse(token_remaining=token_manager.get_token_remaining(), model_name=token_manager.get_model_name())

@app.post("/api/v1/ask")
async def handle_chat(msg: ConversationHistory):
    return StreamingResponse(ask(normalize_conversations(msg.conversation_history), token_manager.get_model_name()), media_type="text/plain")
