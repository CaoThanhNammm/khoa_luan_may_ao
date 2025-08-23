from fastembed import LateInteractionTextEmbedding


class ModelLateInteraction:
    def __init__(self, model_name):
        self.model_name = model_name
        self.embedding_model = self.load_model()
        print("Loaded ColBERT v2 successfully")

    def load_model(self):
        return LateInteractionTextEmbedding(self.model_name)

    def embed(self, texts):
        embeddings = list(self.embedding_model.embed(texts))
        return embeddings