from typing import List
from app.core.config import settings
from app.services.interfaces import Embedder
from openai import OpenAI
import logging


class OpenAIEmbedder(Embedder):
    """
    Implementation of the Embedder interface using OpenAI's embedding API.
    """

    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_embeddings(self, texts: List[str]) -> List[float]:
        """
        Generates embeddings for the given list of texts using OpenAI API.

        Args:
            texts (List[str]): A list of texts to generate embeddings for.

        Returns:
            List[float]: A list of embeddings for the given texts.

        Raises:
            ValueError: If the input is invalid.
            Exception: For any unexpected errors from the OpenAI API.
        """

        try:
            response = self.client.embeddings.create(
                input=texts,
                model="text-embedding-3-small"
            )
            
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Failed to generate embeddings: {e}")
