import requests

async def ask(conversation: list):
    print(conversation)
    prompt = 'You are assistant, you will answer questions related to AI. The following is the conversation history, please answer the last question based on conversation history:\n\n'
    output = ""
    for data in conversation:
        output += f"{prompt} Role: {data['role']}\nContent: {data['content']}\n\n"

    payload = {
        "inputs": output,
        "parameters": {
            "stream": True
        }
    }

    header = {
        "Authorization": "Bearer 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"
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/EleutherAI/gpt-neox-20b",
        json=payload,
        headers=header,
        stream=True
    )

    for chunk in response.iter_lines():
        print(chunk, end='')
        yield chunk
