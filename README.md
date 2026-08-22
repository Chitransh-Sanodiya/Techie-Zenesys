# Ai_Powered_Document_Intelligence
ZENESYS PROJECT<br>
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

workflow


-----------------Step 1--------------------

Create the project files

check version

Create virtual environment

install packages
<br>
-----------------Step 2--------------------

Created databases

conneccted fastapi and mysql

Example execution
<br>
-----------------Step 3--------------------

Updated Backend

Created Key using gemini lite (FREE TIER)

connected Gemini with backend and executed some test cases
<br>
-----------------Step 4--------------------

ERP invoice records

Validation engine

Risk scoring

Connect risk scoring → database/API 

Purchase Order extraction
<br>
-----------------Step 5--------------------

PO ↔ Invoice matching

Automatic PO discovery 

fixed error

updated databases

run 5-6 unique test cases
<br>
-----------------Step 6--------------------

Frontend 

frontend and backend connection
<br>
-----------------Final--------------------

Finalization

ERRoR FIX
