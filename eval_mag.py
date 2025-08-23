import time

from Chat import Chat
from LLM.Gemini import Gemini
import os
from dotenv import load_dotenv
from LLM.Llama import Llama
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from VectorDatabase.Qdrant import Qdrant
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
load_dotenv()
from PreProcessing.PreProcessing import PreProcessing
import pandas as pd


if __name__ == "__main__":
    qa = pd.read_csv(r"D:\dataset_benchmark_khoa_luan\mag\mag_auto_qa.csv")
    pre_processing = PreProcessing()
    # 3. Khởi tạo Qdrant
    host = os.getenv("QDRANT_LOCAL")
    api = os.getenv("API_KEY_QDRANT")
    distance = os.getenv("DISTANCE")
    # 2. Khởi tạo mô hình nhúng
    factory = EmbeddingFactory()
    model_name_512 = os.getenv("MODEL_EMBEDDING_512")
    model_name_768 = os.getenv("MODEL_EMBEDDING_768")
    model_name_1024 = os.getenv("MODEL_EMBEDDING_1024")
    model_name_li = os.getenv("MODEL_LATE_INTERACTION")

    model_512 = factory.create_embed_model(model_name_512)
    model_768 = factory.create_embed_model(model_name_768)
    model_1024 = factory.create_embed_model(model_name_1024)
    model_li = factory.create_embed_model(model_name_li)

    qdrant = Qdrant(
        host,
        api,
        model_1024,
        model_768,
        model_512,
        model_li,
        'vss_prime',
        pre_processing
    )

    # 4. khởi tạo mô hình llama để tạo chunking
    model_llama_405b = os.getenv("MODEL_LLAMA_405B")
    model_llama_70b = os.getenv("MODEL_LLAMA_70B")
    api_key_01 = os.getenv("API_KEY_NVIDIA_01")
    api_key_02 = os.getenv("API_KEY_NVIDIA_02")
    api_key_03 = os.getenv("API_KEY_NVIDIA_03")

    llama_title = Llama(api_key_01, model_llama_70b)
    llama_content = Llama(api_key_02, model_llama_405b)
    llama_chunks = Llama(api_key_03, model_llama_405b)

    # 5. khởi tạo neo4j
    uri = os.getenv("URI_LOCAL")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD_LOCAL")
    neo4j = Neo4j(uri, user, password)

    # 6. khởi tạo chat
    t = 5
    conversation = Chat(t, qdrant, neo4j, pre_processing, 'vss_prime')

    my_qa = pd.DataFrame(columns=['question', 'answer'])
    file_name = 'my_qa_mag_01.csv'

    for index, row in qa[:].iterrows():
        q = row['query']

        try:
            conversation.set_question(q)
            answer = conversation.answer_mag()
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 1 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)
        except:
            conversation = Chat(t, qdrant, neo4j, pre_processing, 'vss_prime')
            conversation.set_question(q)
            answer = conversation.answer_mag()
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 2 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)

    my_qa.to_csv(fr"C:\Users\Nam\Desktop\my_qa_mag_final.csv", encoding='utf-8-sig')
