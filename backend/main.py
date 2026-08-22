from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy.orm import Session

from pathlib import Path
import shutil

from database import get_db
from models import Document

from services.gemini_service import analyze_invoice

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

    # Create uploads folder
    upload_folder = Path("uploads")
    upload_folder.mkdir(exist_ok=True)

    # Save file
    file_path = upload_folder / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create initial database record
    document = Document(
        file_name=file.filename,
        document_type="PROCESSING",
        file_path=str(file_path),
        status="PROCESSING"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:

        # Send document to Gemini
        extracted_data = analyze_invoice(
            str(file_path)
        )

        # Update database
        document.document_type = extracted_data.get(
            "document_type",
            "UNKNOWN"
        )

        document.extracted_data = extracted_data

        document.status = "AI_EXTRACTED"

        db.commit()
        db.refresh(document)

        return {
            "message": "Document processed successfully",
            "document_id": document.id,
            "file_name": document.file_name,
            "document_type": document.document_type,
            "status": document.status,
            "extracted_data": extracted_data
        }

    except Exception as e:

        document.status = "AI_FAILED"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"AI processing failed: {str(e)}"
        )