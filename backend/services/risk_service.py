def calculate_risk_score(
    validation_result: dict,
    invoice_data: dict
):

    score = 0
    reasons = []

    # --------------------------------
    # 1. Validation errors
    # --------------------------------

    errors = validation_result.get("errors", [])

    if errors:

        score += 40

        reasons.append(
            f"{len(errors)} validation error(s) detected"
        )

    # --------------------------------
    # 2. Warnings
    # --------------------------------

    warnings = validation_result.get("warnings", [])

    if warnings:

        score += 15

        reasons.append(
            f"{len(warnings)} warning(s) detected"
        )

    # --------------------------------
    # 3. Missing invoice number
    # --------------------------------

    if not invoice_data.get("invoice_number"):

        score += 20

        reasons.append(
            "Invoice number is missing"
        )

    # --------------------------------
    # 4. Missing vendor
    # --------------------------------

    if not invoice_data.get("vendor"):

        score += 20

        reasons.append(
            "Vendor information is missing"
        )

    # --------------------------------
    # 5. Missing total
    # --------------------------------

    if invoice_data.get("total") is None:

        score += 20

        reasons.append(
            "Invoice total is missing"
        )

    # --------------------------------
    # Maximum score = 100
    # --------------------------------

    score = min(score, 100)

    # --------------------------------
    # Risk level
    # --------------------------------

    if score <= 20:

        level = "LOW"

    elif score <= 50:

        level = "MEDIUM"

    elif score <= 80:

        level = "HIGH"

    else:

        level = "CRITICAL"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
