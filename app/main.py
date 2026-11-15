
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag import answer_question

# Create FastAPI application
app = FastAPI(
    title="Tamil Nadu Farmers AI Assistant",
    description="An AI assistant that answers farmers' questions using government documents.",
    version="1.0.0"
)


# Define the request format
class QuestionRequest(BaseModel):
    question: str
    language: str = "English"


# Define the home endpoint
@app.get("/")
def home():
    return {
        "message": "Tamil Nadu Farmers AI Assistant API is running!"
    }


# Define the health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Define the question-answering endpoint
@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        answer = answer_question(
            question=request.question,
            language=request.language
        )

        return {
            "question": request.question,
            "language": request.language,
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
