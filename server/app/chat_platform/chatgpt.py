from g4f.client import Client
import asyncio

client = Client()

async def ask(msg: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
        stream=True
    )

    print(response)

    for chunk in response:
        if "choices" in chunk:  # Kiểm tra chunk
            content = chunk["choices"][0].message.content
            yield content
            await asyncio.sleep(0.01)
