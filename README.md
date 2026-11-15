# Tamil Nadu Farmers AI Assistant

A bilingual AI-powered agricultural information assistant built using Retrieval-Augmented Generation (RAG). The application helps users access information about government agricultural schemes through an interactive English and Tamil interface.

## 1. Project Objective

The objective is to make government agricultural information easier to access by helping farmers understand:

- Government agricultural schemes
- Scheme benefits and financial assistance
- Eligibility criteria
- Required documents
- Application procedures
- Agricultural price support information

The assistant retrieves relevant information from its indexed knowledge base and generates context-grounded responses.

## 2. Key Features

- **Bilingual Question Answering:** Ask questions in English or Tamil.
- **Government Information Retrieval:** Search indexed agricultural scheme information.
- **PDF Processing:** Extract information and page references from government PDFs.
- **RAG Architecture:** Use multilingual embeddings and FAISS vector search.
- **AI-Powered Responses:** Generate answers using the OpenAI API.
- **Source Attribution:** Display source documents, page references and official links when available.
- **Unsupported Question Handling:** Avoid presenting unsupported information as fact.
- **Interactive Interface:** Streamlit frontend.
- **REST API:** FastAPI backend.

## 3. Technology Stack

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

## 4. System Architecture

1. User enters a question through the Streamlit interface.
2. The frontend sends the question to the FastAPI backend.
3. Tamil questions are translated into English for retrieval.
4. The multilingual embedding model converts the question into a vector representation.
5. FAISS retrieves relevant passages from indexed government information.
6. Retrieved information is passed to the OpenAI language model.
7. The assistant generates a response grounded in the retrieved context.
8. The answer and available source references are displayed.

## 5. Project Structure

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
│   └── Farmers_RAG_Buildathon_Screenshots.pdf
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 6. Setup and Installation

### Prerequisites

- Python 3.13
- Git
- OpenAI API key

### Clone the repository

```bash
git clone https://github.com/SriramRagz/farmers-rag-buildathon.git
cd farmers-rag-buildathon
```

### Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Configure the API key

Create a `.env` file in the project root using `.env.example` as a reference.

Add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

Keep `.env` private. It is excluded from Git using `.gitignore`.

### Build the vector database

Place the required government PDF documents inside `data/pdfs/` and run:

```bash
python -m app.ingest
```

### Start the FastAPI backend

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

### Start the Streamlit frontend

Open another Terminal window:

```bash
cd ~/Buildathon/Farmers-RAG
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Application URL:

http://localhost:8501

## 7. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/ask` | Submit an agricultural question |

## 8. Validation and Testing

The following scenarios were manually tested:

- PM-KISAN annual benefit in English.
- PM-KISAN annual benefit in Tamil.
- Green gram minimum support price for 2026–27.
- Unsupported tractor subsidy question.

The application returned the expected responses for these test scenarios, including government source references where available.

Automated API tests:

```bash
python -m pytest -v
```

Latest recorded test result: 4 tests passed.

## 9. Screenshots and Evidence

The project demonstration and test evidence are available here:

[View Buildathon Screenshots PDF](screenshots/Farmers_RAG_Buildathon_Screenshots.pdf)

The evidence document contains the application interface, bilingual responses, government source references, unsupported-question handling and GitHub repository details.

## 10. Limitations

- The assistant can only answer from information available in its indexed knowledge base.
- Information not found in the indexed sources may result in an unsupported response.
- Government scheme information should always be checked against the latest official notifications.
- The current dataset requires ongoing source verification and updates.

## 11. Future Enhancements

- Expand the collection of verified Tamil Nadu agricultural government documents.
- Add more agricultural schemes and crop-specific information.
- Improve Tamil language retrieval and response quality.
- Introduce automated document updates.
- Add more extensive retrieval and response evaluation.
- Improve accessibility for farmers through a mobile-friendly interface.

## 12. Repository

GitHub:

https://github.com/SriramRagz/farmers-rag-buildathon

---

**Project:** Tamil Nadu Farmers AI Assistant  
**Category:** RAG Buildathon  
**Focus:** AI-powered agricultural information access in English and Tamil
