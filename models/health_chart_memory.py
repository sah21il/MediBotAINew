from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HealthChartMemory:
    def __init__(self, chart_text: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.sentences = [line.strip() for line in chart_text.split("\n") if line.strip()]

        if not self.sentences:
            print("⚠️ No valid chart data found. Using fallback rules.")
            self.sentences = [
                "Normal heart rate: 60–100 bpm",
                "High heart rate above 100 bpm may indicate tachycardia",
                "Low heart rate below 60 bpm may indicate bradycardia",
                "Normal blood pressure around 120/80 mmHg",
                "High blood pressure above 140/90 indicates hypertension"
            ]

        self.embeddings = self.model.encode(self.sentences)

    def recall(self, query: str, top_k: int = 3):
        """Find the most relevant chart rules for a given query."""
        if len(self.embeddings) == 0:
            print("⚠️ No embeddings available for recall. Returning empty list.")
            return []

        q_emb = self.model.encode([query])
        scores = cosine_similarity(q_emb, self.embeddings)[0]
        top_idxs = np.argsort(scores)[::-1][:top_k]
        return [self.sentences[i] for i in top_idxs]
