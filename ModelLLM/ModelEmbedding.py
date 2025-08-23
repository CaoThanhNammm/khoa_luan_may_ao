from sentence_transformers import SentenceTransformer

class ModelEmbedding:
    def __init__(self, name):
        self.name = name
        self.model = self.load_model()

    def load_model(self):
        model = SentenceTransformer(self.name, trust_remote_code=True)
        print(f"load model embedding {self.name} success")
        return model

    def embed(self, text):
        return self.model.encode(text).tolist()