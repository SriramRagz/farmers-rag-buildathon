# Tamil Nadu Farmers AI Assistant

An AI-powered agricultural government schemes assistant built using **Retrieval-Augmented Generation (RAG)**. The application helps farmers access information from government documents through a conversational interface in English and Tamil.

## Project Objective

To make agricultural government scheme information easier to access by helping farmers understand:

- Government agricultural schemes
- Scheme benefits and financial assistance
- Eligibility criteria
- Required documents
- Application procedures

The assistant retrieves information from an indexed knowledge base and generates responses using the retrieved government source content.

## Key Features

- **Bilingual Question Answering:** Ask agricultural questions in English or Tamil.
- **Government Document Retrieval:** Retrieve relevant information from indexed government documents.
- **PDF Processing:** Extract and process information from government PDF documents.
- **RAG Architecture:** Use FAISS vector search and large language models to generate context-based answers.
- **Source Attribution:** Display source filenames and page references when available.
- **Interactive Interface:** Simple Streamlit-based user interface.
- **REST API:** FastAPI backend for question processing.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API |
| Streamlit | User interface |
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
4. The multilingual embedding model and FAISS vector database retrieve relevant document passages.
5. Retrieved information is passed to the OpenAI language model.
6. The assistant generates an answer using the retrieved context.
7. The response and available source references are displayed to the farmer.

## Project Structure

```text
Farmers-RAG/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── ingest.py
│   ├── rag.py
│   └── prompts.py
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── pdfs/
│   ├── processed/
│   └── tn_agriculture_schemes.json
├── vectorstore/
├── tests/
│   └── test_rag.py
├── screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/SriramRagz/farmers-rag-build