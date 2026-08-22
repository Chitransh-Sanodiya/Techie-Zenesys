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
    # TEST MISMATCH
    # =========================

    #invoice_items[0].quantity = 7  #this line is only for a test case dont try to add modify this

    # =========================
    # MATCH
    # =========================

    result = compare_purchase_order_with_invoice(
        purchase_order=purchase_order,
        po_items=po_items,
        invoice=invoice,
        invoice_items=invoice_items
    )

    # =========================
    # PRINT RESULT
    # =========================

    print("\n========== MATCHING RESULT ==========\n")

    print("PO Number:")
    print(purchase_order.po_number)

    print("\nInvoice Number:")
    print(invoice.invoice_number)

    print("\nStatus:")
    print(result["status"])

    print("\nMismatch Count:")
    print(result["mismatch_count"])

    print("\nMismatches:")

    for mismatch in result["mismatches"]:
        print("-", mismatch)

    print("\n=====================================\n")

finally:

    db.close()
