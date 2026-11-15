
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
            "FAISS index not found. Run: python -m app.ingest"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_documents(question: str, k: int = 5):
    """Retrieve relevant passages from indexed government sources."""

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    vectorstore = load_vectorstore()

    return vectorstore.similarity_search(
        question.strip(),
        k=k
    )


def get_source_details(document):
    """Format source information without assuming every source is a PDF."""

    metadata = document.metadata

    source = (
        metadata.get("source")
        or metadata.get("title")
        or metadata.get("source_name")
        or "Unknown source"
    )

    page = metadata.get("page")

    if page is not None:
        return f"Source: {source}, Page: {page}"

    return f"Source: {source}"


def answer_question(question: str, language: str = "English"):
    """Generate a grounded answer using retrieved government information."""

    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is missing. Check your .env file."
        )

    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    if language.lower() not in ["english", "tamil"]:
        raise ValueError("Language must be English or Tamil.")

    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0
    )

    original_question = question.strip()
    search_question = original_question

    # Translate Tamil questions to English for retrieval.
    if language.lower() == "tamil":
        translation_prompt = f"""
Translate this Tamil question into clear English.

Return only the translated question.
Do not answer it.

Question:
{original_question}
"""
        translated = llm.invoke(translation_prompt)
        search_question = translated.content.strip()

    # Retrieve relevant passages from the FAISS index.
    documents = retrieve_documents(search_question, k=5)

    if not documents:
        if language.lower() == "tamil":
            return "மன்னிக்கவும். கிடைக்கும் அரசு ஆவணங்களில் இதற்கான தகவல் இல்லை."
        return (
            "Sorry, I could not find relevant information "
            "in the available government sources."
        )

    # Build context and source references.
    context_parts = []
    source_references = []

    for document in documents:
        source_detail = get_source_details(document)

        context_parts.append(
            f"{source_detail}\n"
            f"Content:\n{document.page_content}"
        )

        if source_detail not in source_references:
            source_references.append(source_detail)

    context = "\n\n".join(context_parts)
    sources = "\n".join(
        f"- {source}" for source in source_references
    )

    prompt = f"""
You are a reliable agricultural information assistant
for farmers in Tamil Nadu.

Answer the farmer's question using ONLY the government
information provided in the context.

STRICT RULES:
1. Never invent scheme details, eligibility, subsidies,
   application dates, amounts or required documents.
2. If the context does not contain the answer, clearly
   state that the information is not available in the
   indexed government sources.
3. Respond in {language}.
4. Use simple language that farmers can understand.
5. Preserve numbers, dates, amounts and conditions accurately.
6. Do not mix details from different schemes.
7. Do not claim a farmer is eligible unless the source
   explicitly supports that conclusion.
8. Mention the relevant source name and page number
   when a page number is available.
9. If a source has no page number, cite its source name.
10. Do not create citations that are not present in the context.

GOVERNMENT SOURCE CONTENT:
{context}

AVAILABLE SOURCE REFERENCES:
{sources}

FARMER'S QUESTION:
{original_question}

Provide a clear and concise answer.
"""

    response = llm.invoke(prompt)

    return response.content
