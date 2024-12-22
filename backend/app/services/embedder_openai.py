from openai import OpenAI
from typing import List
from app.core.config import settings
from app.services.interfaces import EMBEDDER

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

class OpenAIEmbedder(EMBEDDER):

    def get_embeddings(self, texts: List[str]) -> List[float]:
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding