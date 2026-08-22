from database import SessionLocal

from models import (
    PurchaseOrder,
    PurchaseOrderItem,
    Invoice,
    InvoiceItem
)

from services.matching_service import (
    compare_purchase_order_with_invoice
)

from services.match_service import (
    save_match_result
)


db = SessionLocal()

try:

    # =========================
    # GET LATEST PO
    # =========================

    purchase_order = (
        db.query(PurchaseOrder)
        .order_by(PurchaseOrder.id.desc())
        .first()
    )

    if not purchase_order:
        print("No purchase order found.")
        exit()

    # =========================
    # GET PO ITEMS
    # =========================

    po_items = (
        db.query(PurchaseOrderItem)
        .filter(
            PurchaseOrderItem.purchase_order_id
            == purchase_order.id
        )
        .all()
    )

    # =========================
    # GET LATEST INVOICE
    # =========================

    invoice = (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .first()
    )

    if not invoice:
        print("No invoice found.")
        exit()

    # =========================
    # GET INVOICE ITEMS
    # =========================

    invoice_items = (
        db.query(InvoiceItem)
        .filter(
            InvoiceItem.invoice_id
            == invoice.id
        )
        .all()
    )

    # =========================
    # COMPARE
    # =========================

    match_result = compare_purchase_order_with_invoice(
        purchase_order=purchase_order,
        po_items=po_items,
        invoice=invoice,
        invoice_items=invoice_items
    )

    print("\n========== MATCH RESULT ==========\n")
    print(match_result)

    # =========================
    # SAVE RESULT
    # =========================

    saved_match = save_match_result(
        db=db,
        purchase_order_id=purchase_order.id,
        invoice_id=invoice.id,
        match_result=match_result
    )

    print("\n========== SAVED ==========\n")

    print("Match ID:", saved_match.id)
    print("Status:", saved_match.status)
    print("Mismatch Count:", saved_match.mismatch_count)

    print("\n============================\n")

finally:

    db.close()