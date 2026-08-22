CREATE DATABASE IF NOT EXISTS documind_db;

USE documind_db;

-- =========================
-- VENDORS
-- =========================

CREATE TABLE vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- DOCUMENTS
-- =========================

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50),
    file_path VARCHAR(500),
    status VARCHAR(50) DEFAULT 'PROCESSING',
    extracted_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- INVOICES
-- =========================

CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    vendor_id INT,
    invoice_number VARCHAR(100),
    invoice_date DATE,
    subtotal DECIMAL(12,2),
    tax DECIMAL(12,2),
    total DECIMAL(12,2),
    risk_score INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'PENDING',

    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);


-- =========================
-- INVOICE ITEMS
-- =========================

CREATE TABLE invoice_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    product_name VARCHAR(255),
    quantity INT,
    unit_price DECIMAL(12,2),
    total_price DECIMAL(12,2),

    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);


-- =========================
-- PURCHASE ORDERS
-- =========================

CREATE TABLE purchase_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    vendor_id INT,
    po_number VARCHAR(100),
    po_date DATE,
    total DECIMAL(12,2),
    status VARCHAR(50) DEFAULT 'PENDING',

    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);


-- =========================
-- PURCHASE ORDER ITEMS
-- =========================

CREATE TABLE purchase_order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_order_id INT,
    product_name VARCHAR(255),
    quantity INT,
    unit_price DECIMAL(12,2),
    total_price DECIMAL(12,2),

    FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id)
);


-- =========================
-- ANOMALIES
-- =========================

CREATE TABLE anomalies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    anomaly_type VARCHAR(100),
    description TEXT,
    severity VARCHAR(50),
    risk_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (document_id) REFERENCES documents(id)
);

