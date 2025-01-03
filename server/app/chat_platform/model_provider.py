from g4f.client import Client
import asyncio

client = Client()

async def ask(conversation: list, model_name: str):
    response = client.chat.completions.create(
        model=model_name,
        # messages=[{"role": "user", "content": msg}],
        messages=conversation,
        stream=True
    )

    for chunk in response:
        print(chunk.choices[0].delta.content, chunk.choices[0].finish_reason)
        if chunk.choices[0].finish_reason == "stop":
            break

        content = chunk.choices[0].delta.content
        yield content
        await asyncio.sleep(0.1)
