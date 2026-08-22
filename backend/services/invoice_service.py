from decimal import Decimal
from datetime import datetime

from sqlalchemy.orm import Session

from models import Invoice, InvoiceItem, Vendor


# =========================================================
# CLEAN DECIMAL
# =========================================================

def clean_decimal(value):

    if value is None:
        return Decimal("0")

    if isinstance(value, Decimal):
        return value

    value = str(value)

    value = (
        value
        .replace("₹", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace(",", "")
        .strip()
    )

    if not value:
        return Decimal("0")

    return Decimal(value)


# =========================================================
# CLEAN DATE
# =========================================================

def clean_date(value):

    if not value:
        return None

    value = str(value).strip()

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d.%m.%Y",
    ]

    for date_format in formats:

        try:

            parsed_date = datetime.strptime(
                value,
                date_format
            )

            return parsed_date.strftime(
                "%Y-%m-%d"
            )

        except ValueError:
            continue

    return None


# =========================================================
# GET / CREATE VENDOR
# =========================================================

def get_or_create_vendor(
    db: Session,
    vendor_name: str
):

    if not vendor_name:
        vendor_name = "Unknown Vendor"

    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_name == vendor_name
        )
        .first()
    )

    if vendor:
        return vendor

    vendor = Vendor(
        vendor_name=vendor_name
    )

    db.add(vendor)

    db.flush()

    return vendor


# =========================================================
# SAVE INVOICE
# =========================================================

def save_invoice_to_database(
    db: Session,
    document_id: int,
    invoice_data: dict
):

    # -----------------------------------------------------
    # Vendor
    # -----------------------------------------------------

    vendor_name = invoice_data.get(
        "vendor",
        "Unknown Vendor"
    )

    vendor = get_or_create_vendor(
        db=db,
        vendor_name=vendor_name
    )


    # -----------------------------------------------------
    # Invoice date
    # -----------------------------------------------------

    invoice_date = clean_date(
        invoice_data.get(
            "invoice_date"
        )
    )


    # -----------------------------------------------------
    # Create invoice
    # -----------------------------------------------------

    invoice = Invoice(

        document_id=document_id,

        vendor_id=vendor.id,

        invoice_number=invoice_data.get(
            "invoice_number"
        ),

        invoice_date=invoice_date,

        subtotal=clean_decimal(
            invoice_data.get(
                "subtotal"
            )
        ),

        tax=clean_decimal(
            invoice_data.get(
                "tax"
            )
        ),

        total=clean_decimal(
            invoice_data.get(
                "total"
            )
        ),

        risk_score=0,

        status="AI_EXTRACTED"
    )

    db.add(invoice)

    # Get invoice ID
    db.flush()


    # -----------------------------------------------------
    # Invoice Items
    # -----------------------------------------------------

    items = invoice_data.get(
        "items",
        []
    )

    for item in items:

        quantity = item.get(
            "quantity",
            0
        )

        try:
            quantity = int(
                float(
                    str(quantity)
                    .replace(",", "")
                )
            )
        except (ValueError, TypeError):
            quantity = 0


        invoice_item = InvoiceItem(

            invoice_id=invoice.id,

            product_name=item.get(
                "name",
                "Unknown Item"
            ),

            quantity=quantity,

            unit_price=clean_decimal(
                item.get(
                    "unit_price"
                )
            ),

            total_price=clean_decimal(
                item.get(
                    "total_price"
                )
            )
        )

        db.add(invoice_item)


    # -----------------------------------------------------
    # Commit
    # -----------------------------------------------------

    db.commit()

    db.refresh(invoice)

    return invoice