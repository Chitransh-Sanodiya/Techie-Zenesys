from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from models import (
    Vendor,
    PurchaseOrder,
    PurchaseOrderItem
)


def clean_money(value):

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return value

    value = str(value)

    # Remove currency symbols and commas
    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.strip()

    try:
        return Decimal(value)
    except ValueError:
        return None


def clean_date(value):

    if not value:
        return None

    try:
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()

    except ValueError:
        return None


def save_purchase_order_to_database(
    db: Session,
    document_id: int,
    po_data: dict
):

    # -------------------------
    # 1. Find or create vendor
    # -------------------------

    vendor_name = po_data.get("vendor")

    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_name == vendor_name
        )
        .first()
    )

    if vendor is None:

        vendor = Vendor(
            vendor_name=vendor_name
        )

        db.add(vendor)
        db.commit()
        db.refresh(vendor)

    # -------------------------
    # 2. Clean PO date
    # -------------------------

    po_date = clean_date(
        po_data.get("po_date")
    )

    # -------------------------
    # 3. Clean PO total
    # -------------------------

    po_total = clean_money(
        po_data.get("total")
    )

    # -------------------------
    # 4. Create purchase order
    # -------------------------

    purchase_order = PurchaseOrder(
        document_id=document_id,
        vendor_id=vendor.id,
        po_number=po_data.get("po_number"),
        po_date=po_date,
        total=po_total,
        status="AI_EXTRACTED"
    )

    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)

    # -------------------------
    # 5. Create PO items
    # -------------------------

    items = po_data.get("items", [])

    for item in items:

        quantity = item.get("quantity")

        unit_price = clean_money(
            item.get("unit_price")
        )

        total_price = clean_money(
            item.get("total_price")
        )

        po_item = PurchaseOrderItem(
            purchase_order_id=purchase_order.id,
            product_name=item.get("name"),
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )

        db.add(po_item)

    db.commit()

    return purchase_order