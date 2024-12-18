import fastapi
import asyncio
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import ChatRequest, ChatResponse, TokenRemaining, ConversationHistory
from chat_platform import chatgpt


app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def normalize_conversations(conversations: List[ChatRequest]) -> List[dict]:
    return [{"role": c.role, "content": ''.join([''.join(char) for char in c.message])} for c in conversations]

@app.post("/api/v1/ask")
async def handle_chat(msg: ConversationHistory):
    return StreamingResponse(chatgpt.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")
