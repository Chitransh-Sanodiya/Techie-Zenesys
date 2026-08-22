from database import SessionLocal

from models import Invoice

from services.matching_service import (
    process_invoice_matching
)

from services.match_service import (
    save_match_result
)


db = SessionLocal()

try:

    # =========================
    # Get latest invoice
    # =========================

    invoice = (
        db.query(Invoice)
        .order_by(
            Invoice.id.desc()
        )
        .first()
    )

    if not invoice:

        print("No invoice found.")
        exit()

    # =========================
    # Automatic matching
    # =========================

    result = process_invoice_matching(
        db,
        invoice
    )

    print("\n========== COMPLETE MATCHING ==========\n")

    print(
        "Invoice:",
        invoice.invoice_number
    )

    print(
        "PO:",
        result.get("po_number")
    )

    print(
        "Status:",
        result.get("status")
    )

    print(
        "Mismatch Count:",
        result.get("mismatch_count")
    )

    print(
        "Mismatches:",
        result.get("mismatches")
    )

    # =========================
    # Save result
    # =========================

    if result.get("status") != "NO_PO_FOUND":

        saved = save_match_result(
            db=db,
            purchase_order_id=result["purchase_order_id"],
            invoice_id=invoice.id,
            match_result=result
        )

        print(
            "\nSaved Match ID:",
            saved.id
        )

    print(
        "\n========================================\n"
    )

finally:

    db.close()
    