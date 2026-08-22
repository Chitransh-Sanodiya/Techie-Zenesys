from database import SessionLocal

from models import Invoice

from services.matching_service import (
    find_matching_purchase_order
)


db = SessionLocal()

try:

    # Get latest invoice

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

    # Find matching PO

    purchase_order = (
        find_matching_purchase_order(
            db,
            invoice
        )
    )

    print("\n========== AUTOMATIC PO MATCH ==========\n")

    print(
        "Invoice:",
        invoice.invoice_number
    )

    print(
        "Invoice Vendor ID:",
        invoice.vendor_id
    )

    if purchase_order:

        print(
            "Matching PO:",
            purchase_order.po_number
        )

        print(
            "PO Vendor ID:",
            purchase_order.vendor_id
        )

    else:

        print(
            "No matching purchase order found."
        )

    print(
        "\n=========================================\n"
    )

finally:

    db.close()
    