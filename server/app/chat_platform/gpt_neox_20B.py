import requests

async def ask(conversation: list):
    payload = {
        "inputs": conversation,
        "parameters": {
            "stream": True
        }
    }

    header = {
        "Authorization": "Bearer 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"
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt-neox-20b",
        json=payload,
        headers=header,
        stream=True
    )

    for chunk in response.iter_lines():
        print(chunk, end='')
        yield chunk
