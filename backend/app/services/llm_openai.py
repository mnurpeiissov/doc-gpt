from openai import OpenAI
from app.services.interfaces import LLM
from app.core.config import settings
from app.services.fhir import convert_to_fhir
import base64
import json

class OpenAILLM(LLM):
    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI(api_key=settings.OPENAI_API_KEY)

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
            response = self.client.chat.completions.create(
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

    def convert_to_fhir(self, context, user_id):
        system_message = (
            "You are an expert in converting medical JSON data into FHIR-compliant JSON. "
            "Ensure that each field is mapped correctly to the appropriate FHIR resource type. "
            "Use `Patient`, `Condition`, `MedicationRequest`, `CarePlan`, and `Practitioner` as needed. "
            "Use ICD-10 codes where available. Maintain all context details."
        )

        query = "Convert the following structured medical record into FHIR-compliant JSON. Ensure that all relevant fields are mapped correctly:"
        user_message = {"role": "user", "content": []}
        user_message["content"].append({"type": "text", "text": f"{query}\n\nMedical Record JSON:\n{context}"})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    user_message
                ],
                max_tokens=8000,
                temperature=0.0
            )
            
            raw_response = response.choices[0].message.content.strip()

            # Extract JSON
            if "```json" in raw_response:
                json_blocks = raw_response.split("```json")
                for block in json_blocks:
                    if "```" in block:
                        raw_response = block.split("```")[0].strip()
                        break

            parsed_data = json.loads(raw_response)
            return parsed_data

        except Exception as e:
            raise RuntimeError(f"Error generating answer: {e}")


    def parse_json(self, context=None, is_img=False, base64_image=None):
        system_message = (
            "You are a master of parsing textual and image data and converting them into JSON format. "
            "The documents and images will mostly be medical records, and your task is to parse the information "
            "into a structured format and return it as JSON. You should return the response in the original language "
            "of the document and English as well, ensuring JSON format only."
            "You need to classify the document type into following categories: prescription, diagnosis, test_results and uknown. Inlcude the document type in JSON"
        )
        
        query = "Classify the document type, extract structured information and return it in JSON format."
        
        user_message = {"role": "user", "content": []}
        
        if is_img and base64_image:
            user_message["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            })
        
        if context:
            user_message["content"].append({"type": "text", "text": f"Question: {query}\n\nContext:\n{context}"})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    user_message
                ],
                max_tokens=8000,
                temperature=0.0
            )
            raw_response = response.choices[0].message.content.strip()
            print(raw_response)
            if "```json" in raw_response:
                raw_response = raw_response.split("```json")[1].split("```")[0].strip()
            parsed_data = json.loads(raw_response)
            return parsed_data
        except Exception as e:
            raise RuntimeError(f"Error generating answer: {e}")

    def translate_to_language(self, context, language):
            system_message = (
                "You are an expert in translating the data in FHIR format to different languages"
                "Keep the original structure and translate all fields, include the keys as well"
                "Use ICD-10 codes where available. Maintain all context details."
            )

            query = f"Translate the following FHIR into this {language} language. Ensure that all relevant fields are mapped correctly:"
            user_message = {"role": "user", "content": []}
            user_message["content"].append({"type": "text", "text": f"{query}\n\nMedical Record JSON:\n{context}"})

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_message},
                        user_message
                    ],
                    max_tokens=8000,
                    temperature=0.0
                )
                
                raw_response = response.choices[0].message.content.strip()

                # Extract JSON
                if "```json" in raw_response:
                    json_blocks = raw_response.split("```json")
                    for block in json_blocks:
                        if "```" in block:
                            raw_response = block.split("```")[0].strip()
                            break

                parsed_data = json.loads(raw_response)
                return parsed_data

            except Exception as e:
                raise RuntimeError(f"Error generating answer: {e}")