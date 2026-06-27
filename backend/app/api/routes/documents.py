from datetime import datetime

from fastapi import APIRouter, UploadFile, File

from app.db.postgres import AsyncSessionLocal
from app.models import Document
from app.schemas.documents import DocumentResponse
from app.services.document_service import save_document

from app.core.rag.parser import read_pdf
from app.core.rag.chunker import chunk_document

from app.core.rag.embedder import embed_texts
from app.core.vectorstore.qdrant_store import store_chunks

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):

    # -----------------------------
    # Save PDF
    # -----------------------------
    document_id, path = save_document(file)

    print("\n========== DOCUMENT UPLOADED ==========")
    print(f"Document ID : {document_id}")
    print(f"Filename    : {file.filename}")
    print(f"Saved Path  : {path}")

    # -----------------------------
    # Parse PDF
    # -----------------------------
    text = read_pdf(path)

    print(f"Characters Extracted : {len(text)}")

    # -----------------------------
    # Chunk PDF
    # -----------------------------
    chunks = chunk_document(
        text=text,
        doc_id=document_id,
    )
    embeddings = await embed_texts(
    [chunk["text"] for chunk in chunks]
)

    print(f"Generated {len(embeddings)} embeddings")

    await store_chunks(
      chunks=chunks,
      embeddings=embeddings,
)

    print(f"Total Chunks Created : {len(chunks)}")

    if len(chunks) > 0:
        print("\nFirst Chunk Preview:")
        print(chunks[0]["text"][:300])

    # -----------------------------
    # Save Metadata in PostgreSQL
    # -----------------------------
    async with AsyncSessionLocal() as session:

        document = Document(
            id=document_id,
            filename=file.filename,
            status="uploaded",
            created_at=datetime.utcnow(),
        )

        session.add(document)

        await session.commit()

        await session.refresh(document)

    print("========== DONE ==========\n")

    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        status=document.status,
        created_at=document.created_at,
    )