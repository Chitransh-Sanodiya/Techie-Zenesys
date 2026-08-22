from sqlalchemy.orm import Session

from models import DocumentMatch


def save_match_result(
    db: Session,
    purchase_order_id: int,
    invoice_id: int,
    match_result: dict
):

    match = DocumentMatch(
        purchase_order_id=purchase_order_id,
        invoice_id=invoice_id,
        status=match_result.get("status"),
        mismatch_count=match_result.get(
            "mismatch_count",
            0
        ),
        mismatch_details=match_result.get(
            "mismatches",
            []
        )
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match
    