"""
Global instances initialization for the application
Khởi tạo một lần duy nhất tất cả các đối tượng cần thiết khi chạy server
"""
import sys
import os
import boto3
import threading
from dotenv import load_dotenv

# Add the parent directory to the path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(parent_dir)

# Import required modules
from PreProcessing.ProcessingPdf import PDF
from LLM.Llama import Llama
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
from VectorDatabase.Qdrant import Qdrant
from ModelLLM.EmbeddingFactory import EmbeddingFactory
from PreProcessing.PreProcessing import PreProcessing

load_dotenv()

# Global instances
pdf = None
llama_chunks = None
llama_title = None
llama_content = None
qdrant = None
neo = None
pre_processing = None
s3_client = None
_initialized = False
_initialization_lock = threading.Lock()

def initialize_global_instances():
    """Initialize all global instances once when server starts"""
    global pdf, llama_chunks, llama_title, llama_content, qdrant, neo, pre_processing, s3_client, _initialized
    
    # Sử dụng lock để đảm bảo thread-safe
    with _initialization_lock:
        # Double-check locking pattern
        if _initialized:
            print("✅ Global instances already initialized, skipping...")
            return
        
        print("🚀 Initializing global instances...")
        
        # Initialize preprocessing
        pre_processing = PreProcessing()
        print("✅ PreProcessing initialized")
        
        # AWS S3 Configuration
        S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
        S3_REGION = os.getenv('S3_REGION')
        
        # Initialize S3 client
        try:
            s3_client = boto3.client(
                's3',
                region_name=S3_REGION,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            # 1. Khởi tạo đối tượng xử lý PDF
            pdf = PDF(s3_client, '', '', '')
            print("✅ S3 client and PDF initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing S3 client: {str(e)}")
            s3_client = None
        
        # 2. Khởi tạo mô hình nhúng
        try:
            factory = EmbeddingFactory()
            model_name_512 = os.getenv("MODEL_EMBEDDING_512")
            model_name_768 = os.getenv("MODEL_EMBEDDING_768")
            model_name_1024 = os.getenv("MODEL_EMBEDDING_1024")
            model_name_li = os.getenv("MODEL_LATE_INTERACTION")
            
            model_512 = factory.create_embed_model(model_name_512)
            model_768 = factory.create_embed_model(model_name_768)
            model_1024 = factory.create_embed_model(model_name_1024)
            model_li = factory.create_embed_model(model_name_li)
            print("✅ Embedding models initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing embedding models: {str(e)}")
            model_512 = model_768 = model_1024 = model_li = None
        
        # 3. Khởi tạo Qdrant
        try:
            host = os.getenv("HOST_QDRANT")
            api = os.getenv("API_KEY_QDRANT")
            name_collection_df = os.getenv('NAME_COLLECTION_DEFAULT')
            qdrant = Qdrant(
                host,
                api,
                model_1024, 
                model_768, 
                model_512, 
                model_li, 
                name_collection_df,
                pre_processing
            )
            print("✅ Qdrant initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Qdrant: {str(e)}")
            qdrant = None
        
        # 4. Khởi tạo mô hình llama để tạo chunking
        try:
            model_llama_405b = os.getenv("MODEL_LLAMA_405B")
            model_llama_70b = os.getenv("MODEL_LLAMA_70B")
            api_key_01 = os.getenv("API_KEY_NVIDIA_01")
            api_key_02 = os.getenv("API_KEY_NVIDIA_02")
            api_key_03 = os.getenv("API_KEY_NVIDIA_03")
            
            llama_title = Llama(api_key_01, model_llama_70b)
            llama_content = Llama(api_key_02, model_llama_405b)
            llama_chunks = Llama(api_key_03, model_llama_405b)
            print("✅ Llama models initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Llama models: {str(e)}")
            llama_title = llama_content = llama_chunks = None
        
        # 5. khởi tạo neo4j
        try:
            uri = os.getenv("URI_NEO")
            user = 'neo4j'
            password = os.getenv("PASSWORD")
            
            neo = Neo4j(uri, user, password)
            print("✅ Neo4j initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Neo4j: {str(e)}")
            neo = None
        
        # Đánh dấu đã khởi tạo xong
        _initialized = True
        print("🎉 All global instances initialized!")

def get_pdf():
    """Get the global PDF instance"""
    if not _initialized:
        initialize_global_instances()
    if pdf is None:
        raise RuntimeError("PDF instance failed to initialize.")
    return pdf

def get_llama_chunks():
    """Get the global llama_chunks instance"""
    if not _initialized:
        initialize_global_instances()
    if llama_chunks is None:
        raise RuntimeError("Llama chunks instance failed to initialize.")
    return llama_chunks

def get_llama_title():
    """Get the global llama_title instance"""
    if not _initialized:
        initialize_global_instances()
    if llama_title is None:
        raise RuntimeError("Llama title instance failed to initialize.")
    return llama_title

def get_llama_content():
    """Get the global llama_content instance"""
    if not _initialized:
        initialize_global_instances()
    if llama_content is None:
        raise RuntimeError("Llama content instance failed to initialize.")
    return llama_content

def get_qdrant():
    """Get the global Qdrant instance"""
    if not _initialized:
        initialize_global_instances()
    if qdrant is None:
        raise RuntimeError("Qdrant instance failed to initialize.")
    return qdrant

def get_neo():
    """Get the global Neo4j instance"""
    if not _initialized:
        initialize_global_instances()
    if neo is None:
        raise RuntimeError("Neo4j instance failed to initialize.")
    return neo

def get_preprocessing():
    """Get the global PreProcessing instance"""
    if not _initialized:
        initialize_global_instances()
    if pre_processing is None:
        raise RuntimeError("PreProcessing instance failed to initialize.")
    return pre_processing

def get_s3_client():
    """Get the global S3 client instance"""
    if not _initialized:
        initialize_global_instances()
    if s3_client is None:
        raise RuntimeError("S3 client failed to initialize.")
    return s3_client

def is_initialized():
    """Check if global instances have been initialized"""
    return _initialized

def get_initialization_status():
    """Get detailed initialization status for debugging"""
    return {
        "initialized": _initialized,
        "pdf": pdf is not None,
        "llama_chunks": llama_chunks is not None,
        "llama_title": llama_title is not None,
        "llama_content": llama_content is not None,
        "qdrant": qdrant is not None,
        "neo": neo is not None,
        "pre_processing": pre_processing is not None,
        "s3_client": s3_client is not None
    }