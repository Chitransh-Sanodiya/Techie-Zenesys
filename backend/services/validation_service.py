from decimal import Decimal, InvalidOperation


# =========================================================
# CLEAN DECIMAL
# =========================================================

def clean_decimal(value):
    """
    Convert AI-extracted currency values into Decimal.

    Examples:
        45000
        "45000"
        "45,000"
        "45,000.00"
        "₹45,000.00"
    """

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

    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal("0")


# =========================================================
# VALIDATE INVOICE
# =========================================================

def validate_invoice(invoice_data):

    errors = []
    warnings = []

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    invoice_number = invoice_data.get(
        "invoice_number"
    )

    invoice_date = invoice_data.get(
        "invoice_date"
    )

    vendor = invoice_data.get(
        "vendor"
    )

    if not invoice_number:
        errors.append(
            "Invoice number is missing."
        )

    if not invoice_date:
        errors.append(
            "Invoice date is missing."
        )

    if not vendor:
        errors.append(
            "Vendor information is missing."
        )


    # -----------------------------------------------------
    # ITEMS
    # -----------------------------------------------------

    items = invoice_data.get(
        "items",
        []
    )

    calculated_subtotal = Decimal("0")

    for item in items:

        name = item.get(
            "name",
            "Unknown Item"
        )

        quantity = item.get(
            "quantity",
            0
        )

        unit_price = item.get(
            "unit_price",
            0
        )

        total_price = item.get(
            "total_price",
            0
        )

        # ---------------------------------------------
        # Quantity
        # ---------------------------------------------

        try:
            quantity_decimal = Decimal(
                str(quantity)
                .replace(",", "")
            )
        except InvalidOperation:
            quantity_decimal = Decimal("0")

            errors.append(
                f"Invalid quantity for item: {name}"
            )


        # ---------------------------------------------
        # Unit Price
        # ---------------------------------------------

        unit_price_decimal = clean_decimal(
            unit_price
        )


        # ---------------------------------------------
        # Total Price
        # ---------------------------------------------

        total_price_decimal = clean_decimal(
            total_price
        )


        # ---------------------------------------------
        # Calculate expected item total
        # ---------------------------------------------

        expected_total = (
            quantity_decimal *
            unit_price_decimal
        )


        calculated_subtotal += (
            total_price_decimal
        )


        # ---------------------------------------------
        # Check item calculation
        # ---------------------------------------------

        if abs(
            expected_total -
            total_price_decimal
        ) > Decimal("0.01"):

            errors.append(
                f"Item total mismatch for: {name}. "
                f"Expected {expected_total}, "
                f"got {total_price_decimal}."
            )


    # -----------------------------------------------------
    # SUBTOTAL
    # -----------------------------------------------------

    extracted_subtotal = clean_decimal(
        invoice_data.get(
            "subtotal",
            0
        )
    )


    if abs(
        calculated_subtotal -
        extracted_subtotal
    ) > Decimal("0.01"):

        warnings.append(
            f"Subtotal mismatch. "
            f"Calculated {calculated_subtotal}, "
            f"extracted {extracted_subtotal}."
        )


    # -----------------------------------------------------
    # TAX
    # -----------------------------------------------------

    tax = clean_decimal(
        invoice_data.get(
            "tax",
            0
        )
    )


    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    extracted_total = clean_decimal(
        invoice_data.get(
            "total",
            0
        )
    )


    expected_total = (
        extracted_subtotal +
        tax
    )


    if abs(
        expected_total -
        extracted_total
    ) > Decimal("0.01"):

        warnings.append(
            f"Invoice total mismatch. "
            f"Expected {expected_total}, "
            f"extracted {extracted_total}."
        )


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    is_valid = len(errors) == 0

    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "calculated_subtotal": float(
            calculated_subtotal
        ),
        "extracted_subtotal": float(
            extracted_subtotal
        ),
        "tax": float(
            tax
        ),
        "total": float(
            extracted_total
        )
    }