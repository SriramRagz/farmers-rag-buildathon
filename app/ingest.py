
import json
from pathlib import Path

import fitz

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.config import (
    PDF_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


# JSON file containing verified agricultural scheme information
SCHEME_JSON_FILE = PDF_DIR.parent / "tn_agriculture_schemes.json"


def extract_pdf_documents():
    """Extract PDF text while retaining source and page information."""

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(PDF_DIR.glob("*.pdf"))
    documents = []

    for pdf_path in pdf_files:
        print(f"Reading PDF: {pdf_path.name}")

        try:
            with fitz.open(pdf_path) as pdf:
                for page_number, page in enumerate(pdf, start=1):
                    text = page.get_text("text").strip()

                    if text:
                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "source": pdf_path.name,
                                    "source_url": (
                                        "https://www.stationeryprinting.tn.gov.in/extraordinary/2026/360_Ex_II_1_2026.pdf"
                                        if pdf_path.name == "greengram_price_support_2026.pdf"
                                        else ""
                                    ),
                                    "page": page_number,
                                    "content_type": "pdf",
                                },
                            )
                        )

        except Exception as error:
            print(f"Could not read {pdf_path.name}: {error}")

    print(f"Extracted {len(documents)} PDF pages.")
    return documents


def extract_json_documents():
    """Convert structured government scheme records into searchable documents."""

    if not SCHEME_JSON_FILE.exists():
        print(f"Scheme JSON file not found: {SCHEME_JSON_FILE}")
        print("Continuing with PDF documents only.")
        return []

    print(f"Reading scheme data: {SCHEME_JSON_FILE.name}")

    try:
        with open(SCHEME_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(f"Could not read scheme JSON: {error}") from error

    schemes = data.get("schemes", []) if isinstance(data, dict) else data

    if not isinstance(schemes, list):
        raise ValueError(
            "Scheme JSON must contain a list of schemes."
        )

    documents = []

    for scheme in schemes:
        if not isinstance(scheme, dict):
            continue

        scheme_name = scheme.get("scheme_name") or scheme.get("name")

        if not scheme_name:
            print("Skipping a scheme record without a scheme name.")
            continue

        content_lines = [
            f"Scheme Name: {scheme_name}"
        ]

        for field in [
            "department",
            "description",
            "benefits_or_subsidy",
            "eligibility",
            "documents_required",
            "application_process",
            "contact",
        ]:
            value = scheme.get(field)

            if value is not None:
                if isinstance(value, (dict, list)):
                    value = json.dumps(
                        value,
                        ensure_ascii=False
                    )

                content_lines.append(
                    f"{field.replace('_', ' ').title()}: {value}"
                )

        source_url = scheme.get("source_url", "")
        last_verified = scheme.get("last_verified", "")

        if source_url:
            content_lines.append(f"Official Source URL: {source_url}")

        if last_verified:
            content_lines.append(f"Last Verified: {last_verified}")

        documents.append(
            Document(
                page_content="\n".join(content_lines),
                metadata={
                    "source": SCHEME_JSON_FILE.name,
                    "title": str(scheme_name),
                    "source_url": str(source_url),
                    "content_type": "scheme_json",
                },
            )
        )

    print(f"Loaded {len(documents)} scheme records.")
    return documents


def split_documents(documents):
    """Split PDF and JSON documents into searchable chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")
    return chunks


def create_vectorstore(chunks):
    """Generate embeddings and save the combined FAISS index."""

    if not chunks:
        print("No documents available. FAISS index was not created.")
        return None

    print("Loading multilingual embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Creating combined FAISS vector database...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"Vector database saved at: {VECTORSTORE_DIR}")

    return vectorstore


def ingest_documents():
    """Ingest both government PDFs and structured scheme records."""

    print("\nStarting government document ingestion...\n")

    pdf_documents = extract_pdf_documents()
    json_documents = extract_json_documents()

    all_documents = pdf_documents + json_documents

    if not all_documents:
        print("No readable government information found.")
        return

    print(f"\nTotal source documents loaded: {len(all_documents)}")

    chunks = split_documents(all_documents)

    create_vectorstore(chunks)

    print("\nGovernment document ingestion completed.")


if __name__ == "__main__":
    ingest_documents()
