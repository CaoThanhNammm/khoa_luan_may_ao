import os
from dotenv import load_dotenv
from cohere import ClientV2

class CohereChatBot:
    def __init__(self, model="command-a-vision-07-2025", temperature=0.3):
        load_dotenv()
        api_key = os.getenv("API_KEY_COHERE_03")
        if not api_key:
            raise ValueError("API_KEY_COHERE not found in .env file")
        self.client = ClientV2(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def chat(self, user_message: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": user_message}],
            temperature=self.temperature
        )
        # Lấy text từ message content
        return response.message.content[0].text