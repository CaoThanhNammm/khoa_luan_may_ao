import os
from dotenv import load_dotenv

from ModelLLM.ModelEmbedding import ModelEmbedding
from ModelLLM.ModelLateInteraction import ModelLateInteraction
load_dotenv()

class EmbeddingFactory:
    @staticmethod
    def create_embed_model(embed_model_name):
        model_embedding_1024_name = os.getenv("MODEL_EMBEDDING_1024")
        model_embedding_768_name = os.getenv("MODEL_EMBEDDING_768")
        model_embedding_512_name = os.getenv("MODEL_EMBEDDING_512")
        model_late_interaction_name = os.getenv("MODEL_LATE_INTERACTION")

        if embed_model_name == model_embedding_1024_name:
            return ModelEmbedding(embed_model_name)
        elif embed_model_name == model_embedding_768_name:
            return ModelEmbedding(embed_model_name)
        elif embed_model_name == model_embedding_512_name:
            return ModelEmbedding(embed_model_name)
        elif embed_model_name == model_late_interaction_name:
            return ModelLateInteraction(embed_model_name)
        else:
            raise ValueError(f"Không hỗ trợ")