from decimal import Decimal


def validate_invoice(invoice_data: dict):

    errors = []
    warnings = []

    # --------------------------------
    # 1. Validate line item calculations
    # --------------------------------

    calculated_subtotal = Decimal("0")

    for item in invoice_data.get("items", []):

        quantity = item.get("quantity")
        unit_price = item.get("unit_price")
        total_price = item.get("total_price")

        if quantity is None or unit_price is None:
            warnings.append(
                f"Missing quantity or unit price for {item.get('name')}"
            )
            continue

        expected_total = (
            Decimal(str(quantity))
            * Decimal(str(unit_price))
        )

        if total_price is not None:

            actual_total = Decimal(
                str(total_price)
            )

            difference = abs(
                expected_total - actual_total
            )

            if difference > Decimal("0.01"):

                errors.append(
                    f"Item total mismatch: "
                    f"{item.get('name')} "
                    f"expected {expected_total} "
                    f"but found {actual_total}"
                )

        calculated_subtotal += expected_total

    # --------------------------------
    # 2. Validate subtotal
    # --------------------------------

    extracted_subtotal = invoice_data.get("subtotal")

    if extracted_subtotal is not None:

        extracted_subtotal = Decimal(
            str(extracted_subtotal)
        )

        difference = abs(
            calculated_subtotal - extracted_subtotal
        )

        if difference > Decimal("0.01"):

            errors.append(
                f"Subtotal mismatch: "
                f"expected {calculated_subtotal} "
                f"but found {extracted_subtotal}"
            )

    # --------------------------------
    # 3. Validate tax + subtotal
    # --------------------------------

    tax = invoice_data.get("tax")
    total = invoice_data.get("total")

    if (
        extracted_subtotal is not None
        and tax is not None
        and total is not None
    ):

        expected_total = (
            extracted_subtotal
            + Decimal(str(tax))
        )

        actual_total = Decimal(
            str(total)
        )

        difference = abs(
            expected_total - actual_total
        )

        if difference > Decimal("0.01"):

            errors.append(
                f"Grand total mismatch: "
                f"expected {expected_total} "
                f"but found {actual_total}"
            )

    # --------------------------------
    # 4. Determine validation status
    # --------------------------------

    if errors:

        status = "FAILED"

    elif warnings:

        status = "WARNING"

    else:

        status = "PASSED"

    return {
        "status": status,
        "errors": errors,
        "warnings": warnings
    }
