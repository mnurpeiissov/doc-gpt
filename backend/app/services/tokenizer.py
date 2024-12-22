from tiktoken import get_encoding

def split_text_into_chunks(text, max_tokens=1000, overlap=50):
    tokenizer = get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    
    chunks = []
    for i in range(0, len(tokens), max_tokens - overlap):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk))
    
    return chunks
