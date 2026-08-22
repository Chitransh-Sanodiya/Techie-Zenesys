from database import SessionLocal
from models import Document
from services.gemini_service import analyze_purchase_order
from services.po_service import save_purchase_order_to_database


# Create database session
db = SessionLocal()

try:

    # -------------------------
    # 1. Analyze PO with Gemini
    # -------------------------

    file_path = "uploads/sample_po.png"

    po_data = analyze_purchase_order(
        file_path
    )

    print("\n========== GEMINI PO DATA ==========\n")
    print(po_data)

    # -------------------------
    # 2. Create document record
    # -------------------------

    document = Document(
        file_name="sample_po.png",
        document_type="purchase_order",
        file_path=file_path,
        status="AI_EXTRACTED",
        extracted_data=po_data
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # -------------------------
    # 3. Save PO to database
    # -------------------------

    purchase_order = save_purchase_order_to_database(
        db=db,
        document_id=document.id,
        po_data=po_data
    )

    print("\n========== PO SAVED ==========\n")

    print(
        "PO ID:",
        purchase_order.id
    )

    print(
        "PO Number:",
        purchase_order.po_number
    )

    print(
        "Total:",
        purchase_order.total
    )

    print("\n==============================\n")

finally:

    db.close()
