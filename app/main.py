from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.rag import answer_question

app = FastAPI(
    title="Tamil Nadu Farmers AI Assistant",
    description="An AI assistant that answers farmers' questions using government documents.",
    version="1.1.0"
)


class QuestionRequest(BaseModel):
    question: str
    language: str = "English"


@app.get("/")
def home():
    return {
        "message": "Tamil Nadu Farmers AI Assistant API is running!"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        result = answer_question(
            question=request.question,
            language=request.language
        )

        return {
            "question": request.question,
            "language": request.language,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
