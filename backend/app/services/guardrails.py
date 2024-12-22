import re
import uuid
from typing import Dict, List, Optional, Tuple


def validate_answer_references(answer: str, meta_data_list: List[Tuple[str, int, str]]) -> Optional[Dict[str, str]]:
    """
    Validate the references in the generated answer against the metadata list.

    Args:
        answer (str): The generated answer containing references.
        meta_data_list (List[Tuple[str, int, str]]): A list of valid document names, paragraph IDs, and UUID document IDs.

    Returns:
        Optional[Dict[str, str]]: A dictionary with "doc_id" (UUID) and "p_id" (int) if a valid reference is found, otherwise None.
    """
    if not answer.strip():
        return None 
    pattern = r'Document:\s*(.*?),\s*Paragraph:\s*(\d+),\s*Document_id:\s*([a-fA-F0-9\-]{36})'
    matches = re.findall(pattern, answer)
    if not matches:
        return None
    for doc_name, p_id_str, doc_id_str in matches:
        try:
            p_id = int(p_id_str)
            doc_id = str(uuid.UUID(doc_id_str))
            for valid_doc_name, valid_pid, valid_doc_id in meta_data_list:
                if (doc_name.strip().lower() == valid_doc_name.strip().lower() 
                        and p_id == valid_pid 
                        and doc_id == valid_doc_id):
                    return {"doc_id": doc_id, "p_id": p_id}
        except (ValueError, TypeError):
            continue 
    return None  
