import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class GPT:
    def __init__(self, model="gpt-5"):
        self.client = OpenAI(api_key=os.getenv("API_KEY_GPT"))
        self.model = model

    def ask(self, question: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=question
        )
        return response.output_text