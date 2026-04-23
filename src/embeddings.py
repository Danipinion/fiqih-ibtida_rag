import os
from sentence_transformers import SentenceTransformer
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class EmbeddingModel:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_query(self, text):
        return self.model.encode(text).tolist()

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

def get_chroma_embedding_function(model_name="paraphrase-multilingual-MiniLM-L12-v2"):
    """
    Returns a ChromaDB compatible embedding function.
    """
    return SentenceTransformerEmbeddingFunction(model_name=model_name)
