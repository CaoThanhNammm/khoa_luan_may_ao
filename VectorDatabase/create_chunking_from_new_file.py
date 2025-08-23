import os
from dotenv import load_dotenv
from LLM import prompt
from LLM.Llama import Llama
from PreProcessing.PreProcessing import PreProcessing
from PreProcessing.ProcessingPdf import PDF
load_dotenv()
from VectorDatabase.Qdrant import Qdrant
import ast

if __name__ == "__main__":
    folder_pdf = "../data"
    collection_name = os.getenv("NAME_COLLECTION")
    size = os.getenv("SIZE")
    distance = os.getenv("DISTANCE")
    host = os.getenv("HOST_QDRANT")
    api = os.getenv("API_KEY_QDRANT")
    model_llama_405b = os.getenv("MODEL_LLAMA_405B")
    model_llama_70b = os.getenv("MODEL_LLAMA_70B")
    api_key_01 =  os.getenv("API_KEY_NVIDIA_01")
    api_key_02 =  os.getenv("API_KEY_NVIDIA_02")
    pre_processing = PreProcessing()

    qdrant = Qdrant(host, api, None, None, None, None, collection_name, pre_processing)
    pdf = PDF(folder_pdf)
    llama = Llama(api_key_01, model_llama_405b)

    chunks = []
    all_paragraphs = []
    sentences = pdf.read_chunks()

    # sử dụng llama để tự động chia chunk. Ouput là mảng các json [{}, {}, {}]
    llama.set_prompt(prompt.chunking())
    for s in sentences:
        llama.set_text(s)
        chunk_json = llama.generator()
        chunk_json.replace("'", '"')
        print(chunk_json)
        chunks.append(ast.literal_eval(chunk_json))

    # tạo ra mảng chứa các chunk. Ouput là mảng String ['', '', '']
    for chunk in chunks:
        for key, content in chunk.items():
            all_paragraphs.append(content)

    print(all_paragraphs)

    # tạo embedding và lưu vào qdrant
    qdrant.create_embedding(all_paragraphs)







