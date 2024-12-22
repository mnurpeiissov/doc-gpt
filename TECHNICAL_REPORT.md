# Technical Report: Doc GPT

## NOTE

Due to time constraints, I have focused on the functionality and correctness of the application. I have hugely dismissed the security practices. I have hardcoded the OPENAI_API_KEY to the settings, to make it more easily shareable with the person checking the implementation. I am fully aware of the implications of doing this and would gladly discuss how to adhere best practices. In some places I have hardcoded the postgres connection details due to time constraint. Everything is easily fixable, just need a little bit more time. 

## Overview

Doc GPT is a retrieval-augmented question-answering system designed to allow users to upload their documents and ask questions about them. Instead of providing answers from a general knowledge corpus, it uses the content of the uploaded documents to ground its responses. This approach ensures data privacy (no unauthorized sharing of document data) and reduces hallucinations by constraining the language model to the user-provided context.

---

## Used Tech Stack

| **Component**    | **Technology**         |
|-------------------|------------------------|
| **Backend**       | FastAPI               |
| **Frontend**      | ReactJS               |
| **Database**      | PostgreSQL            |
| **Embedder**      | OpenAI Embedder       |
| **LLM**           | OpenAI GPT-4          |

---

## Approach Taken

### Document Ingestion and Vectorization
- **Splitting Documents:** Uploaded documents are split into paragraphs or chunks for efficient storage and retrieval.
- **Generating Embeddings:** Embeddings are generated using models like OpenAI’s `text-embedding-ada-002`, `text-embedding-3-small` for each chunk.
- **Storage:** Embeddings and metadata (document ID, paragraph ID, text, etc.) are stored in PostgreSQL with the `pgvector` extension.

### Retrieval-Augmented Generation (RAG)
- **Query Processing:** User queries are embedded using the same embedding model.
- **Similarity Search:** Relevant paragraphs are retrieved via similarity search in PostgreSQL (using `pgvector`).
- **Contextual Answers:** Retrieved paragraphs are fed into a language model (e.g., GPT-4, GPT-4o-mini) with an instruction to use only the retrieved text.

### Frontend Integration
- **React Frontend:** Provides an interface for file uploads and question submissions.
- **Answer Verification:** Users can view answers and links to the specific document paragraphs for context.

### FastAPI Backend
- **Endpoints:**  Endpoints handle document uploads and queries.
- **Modularity:** The backend is modular for future enhancements, the implementation of LLM model, Vector Store and Embedder could be changed very easily just by implementing the respective abstract classes. 

---

## Challenges Faced and their solutions

### Preventing Hallucinations
- Large language models can produce confident but incorrect statements. Providing retrieved paragraphs as explicit context minimizes hallucinations. Furthermore, additional guardrails (e.g., validating references) further ensure correctness were introduced.

### Double Ingestion
- Ensuring to not double ingest the documents. If there are cases when document is double ingested it would take up more space and increase the search space as well. For now, I have implemented simple yet elegant solution to take the hash of the entire document and check its existence in the database. Indexing the document_hash column would speed up look up time. 

### Chunking & Indexing Large Documents
- Token limits and performance constraints require efficient handling of large documents. Chunking into manageable paragraphs would solve the token limits problem and proper indexing in `pgvector` would enable fast retrieval.


### Parapgraph Retrieval
- Another challenge/problem comes from the fact of storing the documents in paragraphs and when the similarity search return the specific paragraph and it is sent to the LLM for inference, the information needed could be in another paragraph as well. The solution might be to just pass the whole document, but it would take lot more tokens

### Connection pooling
- Access of the vector database. I have approached the connection for vector database as global state of the application, so one must ensure that the connections are thread safe. We cant have only one open connection and share it across users, rather I used connection pool where the pool of connections is there and one connections will be assigned per user and reused afterwards

---

## Future Directions

### User Authentication and Authorization
- Implement role-based access to ensure only authorized users can query their documents.

### Improved Frontend UX
- Enhance document visualization and highlight retrieved paragraphs.
- Provide real-time status updates for background processes like chunking and embedding.

### Scalability and Deployment
- Use container orchestration (Kubernetes) for horizontal scaling of frontend and backend.
- Expand vector store capabilities to handle millions of documents with robust performance.