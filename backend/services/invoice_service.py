from datetime import datetime

from sqlalchemy.orm import Session

from models import Vendor, Invoice, InvoiceItem


def save_invoice_to_database(
    db: Session,
    document_id: int,
    invoice_data: dict
):

    # -------------------------
    # 1. Find or create vendor
    # -------------------------

    vendor_name = invoice_data.get("vendor")

    vendor = (
        db.query(Vendor)
        .filter(Vendor.vendor_name == vendor_name)
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
    # 2. Convert invoice date
    # -------------------------

    invoice_date = invoice_data.get("invoice_date")

    if invoice_date:

        try:
            invoice_date = datetime.strptime(
                invoice_date,
                "%d/%m/%Y"
            ).date()

        except ValueError:
            invoice_date = None

    # -------------------------
    # 3. Create invoice
    # -------------------------

    invoice = Invoice(
        document_id=document_id,
        vendor_id=vendor.id,
        invoice_number=invoice_data.get("invoice_number"),
        invoice_date=invoice_date,
        subtotal=invoice_data.get("subtotal"),
        tax=invoice_data.get("tax"),
        total=invoice_data.get("total"),
        status="AI_EXTRACTED"
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    # -------------------------
    # 4. Create invoice items
    # -------------------------

    items = invoice_data.get("items", [])

    for item in items:

        invoice_item = InvoiceItem(
            invoice_id=invoice.id,
            product_name=item.get("name"),
            quantity=item.get("quantity"),
            unit_price=item.get("unit_price"),
            total_price=item.get("total_price")
        )

        db.add(invoice_item)

    db.commit()

    return invoice