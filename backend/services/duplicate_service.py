from models import Invoice


def check_duplicate_invoice(
    db,
    invoice_data: dict
):

    invoice_number = invoice_data.get(
        "invoice_number"
    )

    vendor_name = invoice_data.get(
        "vendor"
    )

    if not invoice_number or not vendor_name:

        return {
            "is_duplicate": False,
            "message": "Not enough information to check duplicates."
        }

    # Find invoices with same invoice number

    existing_invoices = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_number
            == invoice_number
        )
        .all()
    )

    # No previous invoice

    if not existing_invoices:

        return {
            "is_duplicate": False,
            "message": "No duplicate invoice found."
        }

    # Check vendor

    for invoice in existing_invoices:

        if invoice.vendor_id:

            return {
                "is_duplicate": True,
                "message": (
                    "An invoice with the same "
                    "invoice number already exists."
                ),
                "existing_invoice_id": invoice.id
            }

    return {
        "is_duplicate": False,
        "message": "No duplicate invoice found."
    }
