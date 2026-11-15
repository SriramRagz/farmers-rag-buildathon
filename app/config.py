
from pathlib import Path
import os
from dotenv import load_dotenv

# Find the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")

# Project directories
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
PROCESSED_DIR = DATA_DIR / "processed"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# AI model configuration
LLM_MODEL = "gpt-4o-mini"

# Multilingual embedding model
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Text splitting configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
