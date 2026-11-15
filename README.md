cd ~/Buildathon/Farmers-RAG
source venv/bin/activate

cat > README.md <<'EOF'
# Tamil Nadu Farmers AI Assistant

A bilingual AI-powered agricultural information assistant built using Retrieval-Augmented Generation (RAG). The application helps farmers access information from government agricultural scheme documents through an interactive English and Tamil interface.

## Project Objective

To make government agricultural scheme information easier to access by helping farmers understand:

- Government agricultural schemes
- Scheme benefits and financial assistance
- Eligibility criteria
- Required documents
- Application procedures
- Agricultural price support information

The assistant retrieves relevant information from its indexed government knowledge base and generates context-grounded responses.

## Key Features

- **Bilingual Question Answering:** Ask questions in English or Tamil.
- **Government Document Retrieval:** Search indexed agricultural scheme information.
- **PDF Processing:** Extract text and page references from government PDFs.
- **RAG Architecture:** Use multilingual embeddings and FAISS vector search.
- **AI-Powered Responses:** Generate answers using the OpenAI API.
- **Source Attribution:** Display source documents, page references and official links when available.
- **Unsupported Question Handling:** Avoid presenting unsupported information as fact.
- **Interactive Interface:** Streamlit frontend.
- **REST API:** FastAPI backend.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API |
| Streamlit | Frontend interface |
| LangChain | RAG orchestration |
| FAISS | Vector database |
| Sentence Transformers | Multilingual embeddings |
| OpenAI API | Language model responses |
| PyMuPDF | PDF text extraction |
| Pytest | Automated testing |

## System Architecture

1. Farmer enters a question through the Streamlit interface.
2. The frontend sends the question to the FastAPI backend.
3. Tamil questions are translated into English for retrieval.
4. The multilingual embedding model converts the question into a vector representation.
5. FAISS retrieves relevant passages from the indexed government documents.
6. Retrieved information is passed to the OpenAI language model.
7. The assistant generates a response using the retrieved context.
8. The answer and available government source references are displayed.

## Project Structure

```text
Farmers-RAG/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingest.py
│   ├── main.py
│   ├── prompts.py
│   └── rag.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── pdfs/
│   └── tn_agriculture_schemes.json
├── tests/
│   └── test_rag.py
├── screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md