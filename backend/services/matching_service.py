from decimal import Decimal

from sqlalchemy.orm import Session

from models import DocumentMatch


def normalize_name(name):
    """
    Normalize product names so small differences
    don't prevent matching.
    """

    if not name:
        return ""

    return (
        name.lower()
        .strip()
        .replace("-", " ")
        .replace("_", " ")
    )


def compare_purchase_order_with_invoice(
    purchase_order,
    po_items,
    invoice,
    invoice_items
):

    mismatches = []

    # --------------------------------
    # 1. Compare vendor
    # --------------------------------

    if purchase_order.vendor_id != invoice.vendor_id:

        mismatches.append({
            "type": "VENDOR_MISMATCH",
            "message": "Purchase order and invoice have different vendors."
        })

    # --------------------------------
    # 2. Compare PO items with invoice
    # --------------------------------

    for po_item in po_items:

        po_name = normalize_name(
            po_item.product_name
        )

        matching_invoice_item = None

        for invoice_item in invoice_items:

            invoice_name = normalize_name(
                invoice_item.product_name
            )

            if po_name == invoice_name:

                matching_invoice_item = invoice_item
                break

        # ----------------------------
        # Item missing from invoice
        # ----------------------------

        if matching_invoice_item is None:

            mismatches.append({
                "type": "MISSING_ITEM",
                "product": po_item.product_name,
                "message": (
                    f"{po_item.product_name} "
                    "exists in PO but not in invoice."
                )
            })

            continue

        # ----------------------------
        # Quantity comparison
        # ----------------------------

        if po_item.quantity != matching_invoice_item.quantity:

            mismatches.append({
                "type": "QUANTITY_MISMATCH",
                "product": po_item.product_name,
                "expected": po_item.quantity,
                "actual": matching_invoice_item.quantity,
                "message": (
                    f"PO quantity is {po_item.quantity}, "
                    f"but invoice quantity is "
                    f"{matching_invoice_item.quantity}."
                )
            })

        # ----------------------------
        # Unit price comparison
        # ----------------------------

        po_price = Decimal(
            str(po_item.unit_price)
        )

        invoice_price = Decimal(
            str(matching_invoice_item.unit_price)
        )

        if po_price != invoice_price:

            mismatches.append({
                "type": "PRICE_MISMATCH",
                "product": po_item.product_name,
                "expected": float(po_price),
                "actual": float(invoice_price),
                "message": (
                    f"PO unit price is ₹{po_price}, "
                    f"but invoice unit price is "
                    f"₹{invoice_price}."
                )
            })

    # --------------------------------
    # 3. Check for extra invoice items
    # --------------------------------

    po_product_names = {
        normalize_name(item.product_name)
        for item in po_items
    }

    for invoice_item in invoice_items:

        invoice_name = normalize_name(
            invoice_item.product_name
        )

        if invoice_name not in po_product_names:

            mismatches.append({
                "type": "EXTRA_ITEM",
                "product": invoice_item.product_name,
                "message": (
                    f"{invoice_item.product_name} "
                    "exists in invoice but not in PO."
                )
            })

    # --------------------------------
    # 4. Compare totals
    # --------------------------------

    po_total = Decimal(
        str(purchase_order.total)
    )

    invoice_total = Decimal(
        str(invoice.total)
    )

    if po_total != invoice_total:

        mismatches.append({
            "type": "TOTAL_MISMATCH",
            "expected": float(po_total),
            "actual": float(invoice_total),
            "message": (
                f"PO total is ₹{po_total}, "
                f"but invoice total is ₹{invoice_total}."
            )
        })

    # --------------------------------
    # 5. Overall status
    # --------------------------------

    if mismatches:

        status = "MISMATCH"

    else:

        status = "MATCHED"

    return {
        "status": status,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches
    }
def find_matching_purchase_order(
    db,
    invoice
):

    from models import PurchaseOrder

    # Find purchase orders belonging
    # to the same vendor as the invoice

    purchase_order = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.vendor_id
            == invoice.vendor_id
        )
        .order_by(
            PurchaseOrder.id.desc()
        )
        .first()
    )

    return purchase_order
def process_invoice_matching(
    db,
    invoice
):

    from models import (
        PurchaseOrderItem,
        InvoiceItem
    )

    # --------------------------------
    # 1. Find matching PO
    # --------------------------------

    purchase_order = find_matching_purchase_order(
        db,
        invoice
    )

    if not purchase_order:

        return {
            "status": "NO_PO_FOUND",
            "mismatch_count": 0,
            "mismatches": []
        }

    # --------------------------------
    # 2. Get PO items
    # --------------------------------

    po_items = (
        db.query(PurchaseOrderItem)
        .filter(
            PurchaseOrderItem.purchase_order_id
            == purchase_order.id
        )
        .all()
    )

    # --------------------------------
    # 3. Get Invoice items
    # --------------------------------

    invoice_items = (
        db.query(InvoiceItem)
        .filter(
            InvoiceItem.invoice_id
            == invoice.id
        )
        .all()
    )

    # --------------------------------
    # 4. Compare
    # --------------------------------

    result = compare_purchase_order_with_invoice(
        purchase_order=purchase_order,
        po_items=po_items,
        invoice=invoice,
        invoice_items=invoice_items
    )

    # Add PO information to result

    result["purchase_order_id"] = purchase_order.id
    result["po_number"] = purchase_order.po_number

    return result
