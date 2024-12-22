from openai import OpenAI
from app.services.interfaces import LLM
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAILLM(LLM):

    def generate_answer(self, query: str, context: str) -> str:
        """
        Generate an answer to the query based on the given context using GPT-4 models.

        Args:
            query (str): The user's query.
            context (str): The context to base the answer on.

        Returns:
            str: The generated answer or 'not applicable' if no valid response is found.
        """
        system_message = (
            "You are a helpful assistant. You can only use the provided context to answer the user's question.\n"
            "Answer only if the question explicitly involves information found within the context.\n"
            "Do not answer if just keyword matches without explicit relation to context.\n"
            "Do not answer if the question is vague or loosely related to the context.\n"
            "If the answer is found, provide a concise, accurate response and explicitly reference the document and paragraph with words Document:"" and Paragraph:"" and Document_id:"".\n"
            "If the answer is not found in the context, or the question does not explicitly relate to the context, respond with 'not applicable'."
        )
        user_message = f"Question: {query}\n\nContext:\n{context}\nAnswer:"
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=200,
                temperature=0.0
            )
            answer = response.choices[0].message.content.strip()
            return answer if answer else "not applicable"
        except Exception as e:
            raise RuntimeError(f"Error generating answer: {e}")
