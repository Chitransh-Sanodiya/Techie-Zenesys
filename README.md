# Ai_Powered_Document_Intelligence

# DocuMind AI

DocuMind AI is an AI-powered document intelligence system that automatically processes business documents such as invoices and purchase orders.

It uses Gemini AI to extract structured information from documents and provides validation, risk analysis, duplicate detection, and purchase order–invoice matching.

## Features

- Upload PDF and image documents
- AI-powered invoice extraction
- AI-powered purchase order extraction
- Automatic data validation
- Invoice and PO matching
- Quantity and price mismatch detection
- Duplicate invoice detection
- Risk score calculation
- Vendor management
- MySQL database storage
- Dashboard for viewing processed documents and analytics

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- SQLAlchemy

### AI
- Google Gemini API

### Database
- MySQL

## Project Structure

```text
DocuMind-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── invoice_service.py
│   │   ├── po_service.py
│   │   ├── validation_service.py
│   │   ├── risk_service.py
│   │   └── matching_service.py
│   │
│   ├── models.py
│   ├── database.py
│   ├── main.py
│   └── uploads/
│
└── README.md

HOW IT WORKS

User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
Document Upload
  ↓
Gemini AI
  ↓
Data Extraction
  ↓
Validation
  ↓
Risk Analysis
  ↓
PO ↔ Invoice Matching
  ↓
MySQL Database
  ↓
Dashboard