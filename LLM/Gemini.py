# Google Cloud & Generative AI
import google.generativeai as genai
from fastembed import LateInteractionTextEmbedding
import time
class Gemini:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

        # Cấu hình API key
        genai.configure(api_key=self.api_key)

        # Khởi tạo model
        self.model = genai.GenerativeModel(model_name=self.model_name)
        self.chat = self.model.start_chat()
        print("Load model success")

    def generator(self, text: str) -> str:
        response = self.chat.send_message(text)
        return response.text.strip()