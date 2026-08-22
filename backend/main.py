from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy import func
from models import (
    Document,
    Invoice,
    PurchaseOrder,
    DocumentMatch
)

from sqlalchemy.orm import Session

from pathlib import Path
import shutil

from database import get_db

from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

from services.gemini_service import analyze_invoice

from services.invoice_service import save_invoice_to_database

from services.validation_service import validate_invoice

from services.risk_service import calculate_risk_score

from services.matching_service import process_invoice_matching

from services.match_service import save_match_result

from services.duplicate_service import check_duplicate_invoice

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# DASHBOARD SUMMARY
# =========================

@app.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    total_invoices = db.query(
        Invoice
    ).count()

    total_purchase_orders = db.query(
        PurchaseOrder
    ).count()

    total_value = db.query(
        func.sum(Invoice.total)
    ).scalar() or 0

    high_risk_invoices = db.query(
        Invoice
    ).filter(
        Invoice.risk_score >= 50
    ).count()

    duplicate_invoices = db.query(
        Invoice
    ).filter(
        Invoice.status == "CRITICAL"
    ).count()

    matched_documents = db.query(
        DocumentMatch
    ).filter(
        DocumentMatch.status == "MATCHED"
    ).count()

    mismatched_documents = db.query(
        DocumentMatch
    ).filter(
        DocumentMatch.status == "MISMATCH"
    ).count()

    return {
        "total_invoices": total_invoices,
        "total_purchase_orders": total_purchase_orders,
        "total_invoice_value": float(total_value),
        "high_risk_invoices": high_risk_invoices,
        "duplicate_invoices": duplicate_invoices,
        "matched_documents": matched_documents,
        "mismatched_documents": mismatched_documents
    }

# =========================
# DASHBOARD INVOICES
# =========================

@app.get("/dashboard/invoices")
def dashboard_invoices(
    db: Session = Depends(get_db)
):

    invoices = (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .all()
    )

    return [
        {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "vendor_id": invoice.vendor_id,
            "total": float(invoice.total or 0),
            "risk_score": invoice.risk_score,
            "status": invoice.status
        }
        for invoice in invoices
    ]

# =========================
# DASHBOARD MATCHES
# =========================

@app.get("/dashboard/matches")
def dashboard_matches(
    db: Session = Depends(get_db)
):

    matches = (
        db.query(DocumentMatch)
        .order_by(DocumentMatch.id.desc())
        .all()
    )

    return [
        {
            "id": match.id,
            "purchase_order_id": match.purchase_order_id,
            "invoice_id": match.invoice_id,
            "status": match.status,
            "mismatch_count": match.mismatch_count,
            "mismatches": match.mismatch_details
        }
        for match in matches
    ]

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

        # Validate extracted invoice data
        validation_result = validate_invoice(
            extracted_data
        )
        # Check for duplicate invoice
        duplicate_result = {
            "is_duplicate": False,
            "message": "Duplicate check not applicable."
        }

        if extracted_data.get("document_type") == "invoice":

            duplicate_result = check_duplicate_invoice(
                db=db,
                invoice_data=extracted_data
            )

        # Calculate risk
        risk_result = calculate_risk_score(
            validation_result,
            extracted_data
        )

        # Increase risk if duplicate
        if duplicate_result["is_duplicate"]:

            risk_result["score"] = min(
                risk_result["score"] + 50,
                100
            )

            risk_result["level"] = "CRITICAL"

            risk_result["reasons"].append(
                "Duplicate invoice detected"
            )


        risk_result = calculate_risk_score(
            validation_result,
            extracted_data
        )
        if extracted_data.get("document_type") == "invoice":

            invoice = save_invoice_to_database(
                db=db,
                document_id=document.id,
                invoice_data=extracted_data
            )

            invoice.risk_score = risk_result["score"]
            invoice.status = risk_result["level"]

            db.commit()

            # =========================
            # AUTOMATIC PO MATCHING
            # =========================

            match_result = process_invoice_matching(
                db=db,
                invoice=invoice
            )

            # Save match result if PO exists

            if match_result.get("status") != "NO_PO_FOUND":

                save_match_result(
                    db=db,
                    purchase_order_id=match_result["purchase_order_id"],
                    invoice_id=invoice.id,
                    match_result=match_result
                )

        document.status = "AI_EXTRACTED"

        db.commit()
        db.refresh(document)

        return {
            "message": "Document processed successfully",
            "document_id": document.id,
            "file_name": document.file_name,
            "document_type": document.document_type,
            "status": document.status,
            "extracted_data": extracted_data,
            "validation": validation_result,
            "duplicate": duplicate_result,
            "risk": risk_result,
            "matching": match_result
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        db.rollback()

        document.status = "AI_FAILED"

        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"AI processing failed: {type(e).__name__}: {str(e)}"
        )