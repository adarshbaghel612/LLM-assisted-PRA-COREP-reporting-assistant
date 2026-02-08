from fastapi import APIRouter,Depends
from typing import List
from core.pdf_loader import Load_pdf
from core.text_splitter import splitter
from core.embeddings import get_embeddings
from core.vector_store import init_faiss, add_embeddings
from sqlalchemy.orm import Session


router = APIRouter(prefix="/ingest", tags=["Ingest"])

@router.post("/")
async def ingest_all():
    docs = []

    # PDFs
    docs.extend(Load_pdf())

    # Split
    chunks = splitter(docs)

    # Embeddings
    embeddings = get_embeddings()

    # Save to vector DB
    init_faiss()
    add_embeddings(chunks, embeddings)

    return {
        "status": "Ingestion complete",
        "sources": {
            "pdfs": len(Load_pdf())},
        "total_chunks": len(chunks)
    }