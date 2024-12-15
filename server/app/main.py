import fastapi
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from schemas import ChatRequest, ChatResponse, TokenRemaining
from chat_platform import chatgpt


app = fastapi.FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.post("/api/v1/chat")
async def handle_chat(msg: ChatRequest):

    return StreamingResponse(chatgpt.ask(msg.message), media_type="text/plain")
