import fastapi
import asyncio
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import ChatRequest, ChatResponse, ConversationHistory, TokenResponse
from chat_platform import chatgpt, gpt_neox_20B
from chat_platform.token_manager import TokenManager


app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

token_manager = TokenManager()

def get_model():
    if token_manager.get_chatgpt_token_remaining() < 0:
        model = CHATGPT
    elif token_manager.get_gpt_neox_20B_token_remaining() < 0:
        model = GPT_NEOX
    return model

def normalize_conversations(conversations: List[ChatRequest]) -> List[dict]:
    return [{"role": c.role, "content": ''.join([''.join(char) for char in c.message])} for c in conversations]

@app.put("/api/v1/update_token", response_model=TokenResponse)
async def update_token(req: ConversationHistory, res: ChatResponse, model: str):
    token_manager.update_token_remaining(req.conversation_history, res.response, model)
    model = get_model()

    return TokenResponse(token_remaining=token_manager.get_token_remaining(model), model_name=model)

@app.get("/api/v1/token", response_model=TokenResponse)
async def get_token():
    model = get_model()
    return TokenResponse(token_remaining=token_manager.get_token_remaining(model), model_name=model)

@app.post("/api/v1/ask")
async def handle_chat(msg: ConversationHistory, model: str):
    if model == CHATGPT:
        return StreamingResponse(chatgpt.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")
    elif model == GPT_NEOX:
        return StreamingResponse(gpt_neox_20B.ask(normalize_conversations(msg.conversation_history)), media_type="text/plain")
