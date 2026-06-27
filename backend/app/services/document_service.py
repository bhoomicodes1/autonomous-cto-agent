from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

UPLOAD_DIR = Path("app/storage/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_document(file: UploadFile) -> tuple[str, str]:
    document_id = str(uuid.uuid4())

    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return document_id, str(file_path)