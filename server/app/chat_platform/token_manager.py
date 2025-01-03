import tiktoken
from chat_platform.constants import MODELS_ID

gpt_encoder = tiktoken.get_encoding('cl100k_base')
neox_encoder = tiktoken.get_encoding('gpt2')

class TokenManager():
    def __init__(self):
        if len(MODELS_ID) == 0:
            raise ValueError("models_id cannot be empty")

        self.token_remaining = len(MODELS_ID) * [500]
        self.current_cursor = 0

    def get_token_remaining(self):
        return self.token_remaining[self.current_cursor]

    def get_model_id(self):
        return self.current_cursor

    def get_model_name(self):
        return MODELS_ID[self.current_cursor]

    def update_token_remaining(self, req, res):
        self.token_remaining[self.current_cursor] -= (
            sum(len(gpt_encoder.encode(''.join(token[0] for token in sentence.message))) for sentence in list(req))
            + len(gpt_encoder.encode(res))
        )

        if self.token_remaining[self.current_cursor] < 0:
            self.token_remaining[self.current_cursor] = 0
            self.current_cursor = min(len(MODELS_ID) - 1, self.current_cursor + 1)

