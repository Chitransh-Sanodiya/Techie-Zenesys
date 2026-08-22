from database import SessionLocal

from services.duplicate_service import (
    check_duplicate_invoice
)


db = SessionLocal()

try:

    invoice_data = {
        "invoice_number": "INV-2026-1045",
        "vendor": "TechNova Solutions Pvt. Ltd."
    }

    result = check_duplicate_invoice(
        db,
        invoice_data
    )

    print("\n========== DUPLICATE CHECK ==========\n")

    print(result)

    print(
        "\n=====================================\n"
    )

finally:

    db.close()
    