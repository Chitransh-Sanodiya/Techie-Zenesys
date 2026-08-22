from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, DECIMAL
from sqlalchemy.sql import func

from database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    document_type = Column(String(50))
    file_path = Column(String(500))
    status = Column(String(50), default="PROCESSING")
    extracted_text = Column(Text)
    extracted_data = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer)
    vendor_id = Column(Integer)
    invoice_number = Column(String(100))
    invoice_date = Column(String(50))
    subtotal = Column(DECIMAL(12, 2))
    tax = Column(DECIMAL(12, 2))
    total = Column(DECIMAL(12, 2))
    risk_score = Column(Integer, default=0)
    status = Column(String(50), default="PENDING")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer)
    product_name = Column(String(255))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL(12, 2))
    total_price = Column(DECIMAL(12, 2))

# =========================
# PURCHASE ORDER
# =========================

class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer
    )

    vendor_id = Column(
        Integer
    )

    po_number = Column(
        String(100)
    )

    po_date = Column(
        String(50)
    )

    total = Column(
        DECIMAL(12, 2)
    )

    status = Column(
        String(50),
        default="PENDING"
    )


# =========================
# PURCHASE ORDER ITEM
# =========================

class PurchaseOrderItem(Base):

    __tablename__ = "purchase_order_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    purchase_order_id = Column(
        Integer
    )

    product_name = Column(
        String(255)
    )

    quantity = Column(
        Integer
    )

    unit_price = Column(
        DECIMAL(12, 2)
    )

    total_price = Column(
        DECIMAL(12, 2)
    )