import google.generativeai as genai
import dotenv
import asyncio

dotenv.load_dotenv()
GEMINI_API_KEY = dotenv.get_key("../.env", "GEMINI_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=GEMINI_API_KEY)

async def ask(conversation: list):
    chat = model.start_chat(
        history=[{'role': conv['role'], 'parts': conv['content']} for conv in conversation[:-1]],
    )

    res = chat.send_message(conversation[-1]['content'], stream=True)

    for chunk in res:
        yield chunk.text
        await asyncio.sleep(0.1)
