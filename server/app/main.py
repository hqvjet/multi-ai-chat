import fastapi
import asyncio
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import ChatRequest, ChatResponse, ConversationHistory, TokenResponse
from chat_platform import chatgpt, claudeAI
from chat_platform.token_manager import TokenManager
from chat_platform.constants import CHATGPT, GPT_NEOX, NO_MODEL


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
async def update_token(req: ConversationHistory, res: ChatResponse, model: str):
    token_manager.update_token_remaining(req.conversation_history, res.response, model)
    model = token_manager.get_model()

    return TokenResponse(token_remaining=token_manager.get_token_remaining(model), model_name=model)

@app.get("/api/v1/token", response_model=TokenResponse)
async def get_token():
    model = token_manager.get_model()
    return TokenResponse(token_remaining=token_manager.get_token_remaining(model), model_name=model)

@app.post("/api/v1/ask")
async def handle_chat(msg: ConversationHistory, model: str):
    # if model == CHATGPT:
    #     return StreamingResponse(chatgpt.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")
    # else:
    #     return NO_MODEL
    # return StreamingResponse(gemini.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")

    # return StreamingResponse(gemini.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")
    return StreamingResponse(claudeAI.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")

