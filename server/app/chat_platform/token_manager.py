import tiktoken
from chat_platform.constants import CHATGPT, GPT_NEOX, NO_MODEL

gpt_encoder = tiktoken.get_encoding('cl100k_base')
neox_encoder = tiktoken.get_encoding('gpt2')

class TokenManager():
    def __init__(self):
        self.chatgpt_token_remaining = 150
        self.gpt_neox_20B_token_remaining = 150

    def get_token_remaining(self, model: str):
        if model == CHATGPT:
            return self.chatgpt_token_remaining
        elif model == GPT_NEOX:
            return self.gpt_neox_20B_token_remaining
        else:
            return 0

    def get_model(self):
        if self.chatgpt_token_remaining > 0:
            model = CHATGPT
        elif self.gpt_neox_20B_token_remaining > 0:
            model = GPT_NEOX
        else:
            model = NO_MODEL

        return model

    def update_token_remaining(self, req, res, model):
        if model == CHATGPT:
            self.chatgpt_token_remaining -= (
                sum(len(gpt_encoder.encode(''.join(token[0] for token in sentence.message))) for sentence in list(req))
                + len(gpt_encoder.encode(res))
            )
        elif model == GPT_NEOX:
            self.gpt_neox_20B_token_remaining -= (
                sum(len(neox_encoder.encode(''.join(token[0] for token in sentence.message))) for sentence in list(req))
                + len(neox_encoder.encode(res))
            )

