from sentence_transformers import SentenceTransformer, util
import torch
from typing import List, Dict

class Validator:
    def __init__(self, model_embedding, batch_size: int = 16):
        self.model_embedding = model_embedding
        self.batch_size = batch_size

    def _cosine_sim(self, vec1, vec2) -> float:
        return util.cos_sim(vec1, vec2).item()

    def encode(self, texts: List[str], normalize: bool = True):
        """Encode danh sách text với batch"""
        return self.model_embedding.embed(
            texts
        )

    def evaluate(self, question: str, answer: str, documents: List[str]) -> Dict[str, float]:
        # Encode Q, A, D
        q_emb = self.encode([question])
        a_emb = self.encode([answer])
        d_embs = self.encode(documents)

        # 1. Similarity Q–A
        qa_sim = self._cosine_sim(q_emb, a_emb)

        # 2. Q in D (max sim giữa Q và D[i])
        qd_sims = util.cos_sim(q_emb, d_embs)[0]
        qd_max = torch.max(qd_sims).item()

        # 3. A in D (max sim giữa A và D[i])
        ad_sims = util.cos_sim(a_emb, d_embs)[0]
        ad_max = torch.max(ad_sims).item()

        return {
            "QA_similarity": qa_sim,
            "Q_in_D_max": qd_max,
            "A_in_D_max": ad_max,
        }

