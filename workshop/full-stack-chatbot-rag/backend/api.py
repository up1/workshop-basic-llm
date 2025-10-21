"""this module is an FASTAPI server that enable users to ask questions and get answers based on the uploaded document."""

# import required libraries
import logging
from typing import List

from chatbot import ask_question, parse_pdf, retrieve_document, store_document
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create FastAPI instance
app = FastAPI(
    title="Chatbot RAG",
    description="A simple chatbot using OpenAI. to enable asking questions and getting answers based on the uploaded document.",
    version="0.1",
)


#  define the response and request models
class DocumentResponse(BaseModel):
    """Response model for the document API."""

    documents: List
    total: int
    query: str
    error: str = None


class DocumentUploadResponse(BaseModel):
    """Response model for the document upload API."""

    documents: List
    total: int
    status: str
    error: str = None


class AskResponse(BaseModel):
    """Response model for the ask API."""

    query: str
    answer: str
    error: str = None


# define the API endpoints
# define the root endpoint to check the status of the service
@app.get("/")
def read_root():
    return {
        "service": "RAG Chatbot using OPENAI",
        "description": "Welcome to Chatbot RAG API",
        "status": "running",
    }


#  define the document search endpoint to search documents based on the query
@app.get("/documents/{query}")
def search_documents(query: str) -> DocumentResponse:
    """Search documents based on the query."""
    try:
        documents = retrieve_document(query)
        return {"documents": documents, "total": len(documents), query: query}
    except Exception as e:
        logger.error(f"Error searching documents: {e}", exc_info=True)
        return {"error": str(e), "documents": [], "total": 0, query: query}


# define the document upload endpoint to upload documents
@app.post("/documents")
async def upload_documents(files: List[UploadFile]) -> DocumentUploadResponse:
    """Store documents."""
    try:
        documents = []
        for file in files:
            if file.content_type != "application/pdf":
                logger.error(f"Unsupported file type: {file.content_type}")
                raise ValueError("Only PDF files are supported")
            content = await file.read()
            parsed_docs = parse_pdf(content)
            documents.extend(parsed_docs)
        status = store_document(documents)
        return {"documents": documents, "total": len(documents), "status": status}
    except Exception as e:
        logger.error(f"Error uploading documents: {e}", exc_info=True)
        return {"error": str(e), "status": "failed", "documents": [], "total": 0}


# define the ask endpoint to ask questions to the chatbot
@app.get("/ask")
def ask(query: str) -> AskResponse:
    """Ask questions to the chatbot."""
    try:
        answer = ask_question(query)
        return {"query": query, "answer": answer}
    except Exception as e:
        logger.error(f"Error asking question: {e}", exc_info=True)
        return {"error": str(e), "query": query, "answer": ""}