from services.validation_service import validate_invoice


invoice = {
    "document_type": "invoice",
    "invoice_number": "INV-2026-1045",
    "vendor": "TechNova Solutions Pvt. Ltd.",
    "subtotal": 278000,
    "tax": 50040,
    "total": 328040,

    "items": [
        {
            "name": "Dell Latitude Business Laptop",
            "quantity": 5,
            "unit_price": 45000,
            "total_price": 225000
        },
        {
            "name": "Logitech Wireless Mouse",
            "quantity": 10,
            "unit_price": 800,
            "total_price": 8000
        },
        {
            "name": "USB-C Docking Station",
            "quantity": 5,
            "unit_price": 6000,
            "total_price": 30000
        },
        {
            "name": "Wireless Keyboard",
            "quantity": 10,
            "unit_price": 1500,
            "total_price": 15000
        }
    ]
}


result = validate_invoice(invoice)


print("\n========== VALIDATION RESULT ==========\n")

print("Status:", result["status"])

print("\nErrors:")

for error in result["errors"]:
    print("-", error)


print("\nWarnings:")

for warning in result["warnings"]:
    print("-", warning)


print("\n=======================================\n")
