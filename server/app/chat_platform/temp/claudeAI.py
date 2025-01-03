import requests
import dotenv
import asyncio

dotenv.load_dotenv()
SEGMIND_API_KEY = dotenv.get_key("../.env", "SEGMIND_KEY")
URL = "https://api.segmind.com/v1/claude-3.5-sonnet"

async def ask(conversation: list):
    data = {
        "instruction": "Below is conversation history of assistant and user, keep the conversation going.",
        "temperature": 0.1,
        "messages": conversation
    }

    response = requests.post(URL, json=data, headers={'x-api-key': SEGMIND_API_KEY}, stream=True)
    response = response.json()

    for res in response['content'][0]['text'].split(' '):
        yield res + ' '
        await asyncio.sleep(0.2)


