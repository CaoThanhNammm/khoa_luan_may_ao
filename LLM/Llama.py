from openai import OpenAI

class Llama:
    def __init__(self, api_key, model_name):
        self.model_name = model_name
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        self.text = ""
        self.prompt = ""

    def set_text(self, text):
        self.text = text

    def set_prompt(self, prompt):
        self.prompt = prompt

    def generator(self):
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": f"{self.prompt}"},
                {"role": "user", "content": f"{self.text}"}
            ],
            temperature=0.2,
            top_p=0.9,
            max_tokens=4096
        )
        return completion.choices[0].message.content