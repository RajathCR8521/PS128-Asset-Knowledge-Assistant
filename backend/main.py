from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.rag import initialize_rag, answer_question


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="PS128 Asset Knowledge Assistant",
    description=(
        "RAG-based knowledge assistant for "
        "energy and utilities technical documentation."
    ),
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "PS128 Asset Knowledge Assistant API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PS128 Asset Knowledge Assistant"
    }


# ============================================================
# INITIALIZE KNOWLEDGE BASE
# ============================================================

@app.post("/initialize")
def initialize():
    try:

        result = initialize_rag()

        return {
            "message": "Knowledge base initialized successfully",
            "documents": result["documents"],
            "chunks": result["chunks"],
            "embedding_dimension": result["embedding_dimension"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:

        if not request.question.strip():

            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )

        result = answer_question(
            request.question
        )

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )