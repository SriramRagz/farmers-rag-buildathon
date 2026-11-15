
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from app.config import (
    EMBEDDING_MODEL,
    VECTORSTORE_DIR,
    OPENAI_API_KEY,
    LLM_MODEL
)


def load_vectorstore():
    """Load the existing FAISS vector database."""

    index_file = Path(VECTORSTORE_DIR) / "index.faiss"

    if not index_file.exists():
        raise FileNotFoundError(
            "FAISS index not found. Please run: python -m app.ingest"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


def retrieve_documents(question: str, k: int = 3):
    """Find relevant passages from government PDFs."""

    if not question.strip():
        raise ValueError("Please enter a question.")

    vectorstore = load_vectorstore()

    documents = vectorstore.similarity_search(
        question,
        k=k
    )

    return documents


def answer_question(question: str, language: str = "English"):
    """Generate a grounded answer in the requested language."""

    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing. Check your .env file.")

    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0
    )

    search_question = question

    # Translate Tamil questions into English for document retrieval.
    if language.lower() == "tamil":
        translation_prompt = f"""
Translate the following Tamil question into clear English.
Return only the translated question.
Do not answer the question.

Tamil question:
{question}
"""
        translated = llm.invoke(translation_prompt)
        search_question = translated.content.strip()

    # Retrieve passages using the English search question.
    documents = retrieve_documents(search_question, k=3)

    if not documents:
        return "I could not find relevant information in the available documents."

    context = ""

    for doc in documents:
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "Unknown page")

        context += (
            f"\nSource: {source}, Page: {page}\n"
            f"{doc.page_content}\n"
        )

    prompt = f"""
You are a helpful agricultural information assistant for farmers in Tamil Nadu.

Answer the farmer's question using ONLY the government document content below.

Rules:
1. Do not invent facts or scheme details.
2. If the documents do not contain the answer, clearly say so.
3. Respond in {language}.
4. Keep the answer simple and easy for farmers to understand.
5. Include the source document name and page number.
6. Preserve important numbers, dates and amounts accurately.

Government document content:
{context}

Farmer's original question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content
