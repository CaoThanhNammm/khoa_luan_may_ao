import os
from dotenv import load_dotenv
from fastembed import LateInteractionTextEmbedding

from LLM import prompt
from LLM.Llama import Llama
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from PreProcessing.PreProcessing import PreProcessing
from PreProcessing.ProcessingPdf import PDF
load_dotenv()
from VectorDatabase.Qdrant import Qdrant
import ast
import json

if __name__ == "__main__":
    collection_name = 'vmlu_vi_squad'
    size = os.getenv("SIZE")
    distance = os.getenv("DISTANCE")
    host = os.getenv("QDRANT_LOCAL")
    api = os.getenv("API_KEY_QDRANT")
    model_llama_405b = os.getenv("MODEL_LLAMA_405B")
    model_llama_70b = os.getenv("MODEL_LLAMA_70B")
    api_key_01 =  os.getenv("API_KEY_NVIDIA_01")
    api_key_02 =  os.getenv("API_KEY_NVIDIA_02")
    pre_processing = PreProcessing()
    factory = EmbeddingFactory()
    model_name_512 = os.getenv("MODEL_EMBEDDING_512")
    model_name_768 = os.getenv("MODEL_EMBEDDING_768")
    model_name_1024 = os.getenv("MODEL_EMBEDDING_1024")
    model_name_li = os.getenv("MODEL_LATE_INTERACTION")

    model_512 = factory.create_embed_model(model_name_512)
    model_768 = factory.create_embed_model(model_name_768)
    model_1024 = factory.create_embed_model(model_name_1024)
    model_li = factory.create_embed_model(model_name_li)

    qdrant = Qdrant(host, api, model_1024, model_768, model_512, model_li, collection_name, pre_processing)

    qdrant.create_collection("Cosine")
    with open(r"C:\Users\Nam\Downloads\vlmu_squad_v1\vi_squad_benchmark_question_only.json", 'r', encoding='utf-8-sig') as f:
        data = json.loads(f.read())
    data = data['data']

    chunks = []

    for d in data:
        context = d['context']
        chunks.append(context)
    embeddings = qdrant.create_embed(chunks)









