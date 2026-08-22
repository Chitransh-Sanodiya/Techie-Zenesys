from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from database import get_db
from models import Document

app = FastAPI()


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "DocuMind AI Backend is running!"
    }


# =========================
# GET ALL DOCUMENTS
# =========================

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):

    documents = db.query(Document).all()

    return documents


# =========================
# UPLOAD DOCUMENT
# =========================

@app.post("/documents/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Allowed file types
    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg"
    }

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are allowed."
        )

    # Create uploads folder if it doesn't exist
    upload_folder = Path("uploads")
    upload_folder.mkdir(exist_ok=True)

    # File path
    file_path = upload_folder / file.filename

    # Save uploaded file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create database record
    document = Document(
        file_name=file.filename,
        document_type="UNKNOWN",
        file_path=str(file_path),
        status="UPLOADED"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "file_name": document.file_name,
        "status": document.status
    }