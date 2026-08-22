from services.risk_service import calculate_risk_score


# -----------------------------
# GOOD INVOICE
# -----------------------------

good_invoice = {
    "invoice_number": "INV-2026-1045",
    "vendor": "TechNova Solutions Pvt. Ltd.",
    "total": 328040
}

good_validation = {
    "status": "PASSED",
    "errors": [],
    "warnings": []
}


result = calculate_risk_score(
    good_validation,
    good_invoice
)


print("\n========== GOOD INVOICE ==========")
print(result)


# -----------------------------
# BAD INVOICE
# -----------------------------

bad_invoice = {
    "invoice_number": None,
    "vendor": None,
    "total": 400000
}

bad_validation = {
    "status": "FAILED",
    "errors": [
        "Grand total mismatch"
    ],
    "warnings": []
}


result = calculate_risk_score(
    bad_validation,
    bad_invoice
)


print("\n========== BAD INVOICE ==========")
print(result)
