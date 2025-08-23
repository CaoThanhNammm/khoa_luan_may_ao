from qdrant_client.models import PointStruct
from dotenv import load_dotenv
load_dotenv()
from langchain_nvidia_ai_endpoints import NVIDIARerank
from langchain_core.documents import Document
from qdrant_client import models
from qdrant_client import QdrantClient
import os


class Qdrant:
    def __init__(self, host: str, api: str, model_1024, model_768, model_512, model_late_interaction, collection_name: str, pre_processing):
        self.client = QdrantClient(
            url=host,
            api_key=api,
            timeout=1200
        )

        self.collection_name = collection_name
        self.model_1024 = model_1024
        self.model_768 = model_768
        self.model_512 = model_512
        self.model_late_interaction = model_late_interaction
        self.pre_processing = pre_processing

    def create_collection(self):
        if self.client.collection_exists(collection_name=self.collection_name):
            print("Collection đã tồn tại")
            return

        hnsw_config = {
            "m": 16,  # Số kết nối tối đa cho mỗi nút trong đồ thị (mặc định: 16)
            "ef_construct": 1000,  # Yếu tố xây dựng, ảnh hưởng đến chất lượng index (mặc định: 100)
            "full_scan_threshold": 10000  # Ngưỡng để chuyển sang quét toàn bộ nếu tập dữ liệu nhỏ
        }

        # Tạo collection với cấu hình vectors và HNSW
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                'matryoshka-1024dim': models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE,
                    datatype=models.Datatype.FLOAT32
                ),
                'matryoshka-768dim': models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE,
                    datatype=models.Datatype.FLOAT32
                ),
                'matryoshka-512dim': models.VectorParams(
                    size=512,
                    distance=models.Distance.COSINE,
                    datatype=models.Datatype.FLOAT32
                ),
                'late_interaction': models.VectorParams(
                    size=128,
                    distance=models.Distance.COSINE,
                    multivector_config=models.MultiVectorConfig(
                        comparator=models.MultiVectorComparator.MAX_SIM
                    )
                )
            },
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True,
                ),
            ),
            hnsw_config=hnsw_config  # Thêm cấu hình HNSW
        )
        print("create collection success")
        return self.client

    def create_embed(self, chunks):
        """Nhúng toàn bộ văn bản trong chunks một lần theo batch và trả về dict các embedding."""
        print("Starting full-batch embedding...")

        try:
            preprocessed_chunks = [
                self.pre_processing.text_preprocessing_vietnamese(chunk)
                for chunk in chunks
            ]

            # Tạo embedding toàn bộ 1 lần
            embeddings_dict = {
                'matryoshka-1024dim': self.model_1024.embed(preprocessed_chunks),
                'matryoshka-768dim': self.model_768.embed(preprocessed_chunks),
                'matryoshka-512dim': self.model_512.embed(preprocessed_chunks),
                'late_interaction': self.model_late_interaction.embed(preprocessed_chunks)
            }

            print("Embedding completed.")
            return embeddings_dict

        except Exception as e:
            print(f"Lỗi khi tạo embedding toàn bộ: {e}")
            return None

    def add_data(self, chunks, embeddings_dict, batch_size=5):
        """Lưu embedding vào Qdrant theo batch từ dict embeddings đã tạo."""
        if embeddings_dict is None:
            print("No embeddings to upsert.")
            return

        print("Starting upsert into Qdrant...")

        points = []

        for idx in range(len(chunks)):
            point = PointStruct(
                id=idx + 1,
                payload={"text": chunks[idx]},
                vector={
                    'matryoshka-1024dim': embeddings_dict['matryoshka-1024dim'][idx],
                    'matryoshka-768dim': embeddings_dict['matryoshka-768dim'][idx],
                    'matryoshka-512dim': embeddings_dict['matryoshka-512dim'][idx],
                    'late_interaction': embeddings_dict['late_interaction'][idx]
                }
            )
            points.append(point)

            if len(points) >= batch_size:
                self._upsert_points(points)
                print(f"Upserted chunks {idx - batch_size + 2} to {idx + 1}")
                points.clear()

        # Upsert phần còn lại
        if points:
            self._upsert_points(points)
            print(f"Upserted chunks {len(chunks) - len(points) + 1} to {len(chunks)}")

        print("Upsert completed.")

    def _upsert_points(self, points):
        """Helper method để upsert points vào VDB"""
        try:
            self.client.upsert(self.collection_name, points)
            print(f"Upserted {len(points)} points to VDB")
        except Exception as e:
            print(f"Error upserting points: {e}")

    def query_from_db(self, text):
        # Embed văn bản với các mô hình khác nhau
        text_embedded_512 = self.model_512.embed(text)
        text_embedded_768 = self.model_768.embed(text)
        text_embedded_1024 = self.model_1024.embed(text)
        embedded_late_interaction = self.model_late_interaction.embed(text)[0].tolist()

        # Gửi truy vấn đến Qdrant client với các mức embedding khác nhau
        print(self.collection_name)
        response = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=models.Prefetch(
                prefetch=models.Prefetch(
                    prefetch=models.Prefetch(
                        query=text_embedded_512,
                        using="matryoshka-512dim",
                        limit=200,
                    ),
                    query=text_embedded_768,
                    using="matryoshka-768dim",
                    limit=100,
                ),
                query=text_embedded_1024,
                using="matryoshka-1024dim",
                limit=50,
            ),
            query=embedded_late_interaction,
            using="late_interaction",
            limit=25,
        )

        # Lấy kết quả văn bản từ payload
        documents = [point.payload["text"] for point in response.points]
        return documents


    def query_from_db_prime(self, text):
        # Embed văn bản với các mô hình khác nhau
        text_embedded_512 = self.model_512.embed(text)
        text_embedded_768 = self.model_768.embed(text)
        text_embedded_1024 = self.model_1024.embed(text)

        # Gửi truy vấn đến Qdrant client với các mức embedding khác nhau
        print(self.collection_name)
        response = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=models.Prefetch(
                prefetch=models.Prefetch(
                    query=text_embedded_512,
                    using="matryoshka-512dim",
                    limit=200,
                ),
                query=text_embedded_768,
                using="matryoshka-768dim",
                limit=100,
            ),
            query=text_embedded_1024,
            using="matryoshka-1024dim",
            limit=50,
        )

        # Lấy kết quả văn bản từ payload
        documents = [point.payload["text"] for point in response.points]
        return documents

    def re_ranking(self, query, passages):
        client = NVIDIARerank(
            model="nvidia/llama-3.2-nv-rerankqa-1b-v2",
            api_key=os.getenv('API_KEY_NVIDIA_04'),

            top_n=len(passages)
        )

        response = client.compress_documents(
            query=query,
            documents=[Document(page_content=passage) for passage in passages]
        )

        return response

    def set_collection_name(self, name):
        self.collection_name = name

    def get_model_512(self):
        return self.model_512

    def get_model_768(self):
        return self.model_768

    def get_model_1024(self):
        return self.model_1024