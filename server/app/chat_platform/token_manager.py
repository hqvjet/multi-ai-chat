import tiktoken
from constants import CHATGPT, GPT_NEOX

gpt_encoder = tiktoken.get_encoding('cl100k_base')
neox_encoder = tiktoken.get_encoding('gpt2')

class TokenManager():
    def __init__(self):
        self.chatgpt_token_remaining = 150
        self.gpt_neox_20B_token_remaining = 150

    def get_token_remaining(self, model: str):
        if model == CHATGPT:
            return self.chatgpt_token_remaining
        if model == GPT_NEOX:
            return self.gpt_neox_20B_token_remaining

    def update_token_remaining(self, req, res, model):
        if model == CHATGPT:
            self.chatgpt_token_remaining -= len(gpt_encoder.encode(req)) + len(gpt_encoder.encode(res))
        elif model == GPT_NEOX:
            self.gpt_neox_20B_token_remaining -= len(neox_encoder.encode(req)) + len(neox_encoder.encode(res))

