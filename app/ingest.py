
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


def extract_pdf_documents():
    """Extract text from each PDF and retain its source and page number."""

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {PDF_DIR}")
        return []

    documents = []

    for pdf_path in pdf_files:
        print(f"Reading: {pdf_path.name}")

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
                                    "page": page_number,
                                },
                            )
                        )

        except Exception as error:
            print(f"Could not read {pdf_path.name}: {error}")

    return documents


def split_documents(documents):
    """Split extracted PDF text into smaller searchable chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    return chunks


def create_vectorstore(chunks):
    """Convert text chunks into embeddings and save them in FAISS."""

    if not chunks:
        print("No text chunks available. Vector store was not created.")
        return None

    print("Loading multilingual embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Creating FAISS vector database...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore.save_local(str(VECTORSTORE_DIR))

    print(f"Vector database saved at: {VECTORSTORE_DIR}")

    return vectorstore


def ingest_pdfs():
    """Run the complete PDF ingestion pipeline."""

    print("\nStarting PDF ingestion...\n")

    documents = extract_pdf_documents()

    if not documents:
        print("No readable PDF content found.")
        return

    print(f"Extracted text from {len(documents)} PDF pages.")

    chunks = split_documents(documents)

    create_vectorstore(chunks)

    print("\nPDF ingestion completed successfully.")


if __name__ == "__main__":
    ingest_pdfs()
