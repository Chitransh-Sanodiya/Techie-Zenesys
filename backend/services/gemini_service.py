import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env")


client = genai.Client(api_key=API_KEY)


def analyze_invoice(file_path: str):

    # Upload the PDF/image to Gemini
    uploaded_file = client.files.upload(
        file=file_path
    )

    prompt = """
You are an AI business document intelligence system.

Analyze the uploaded business document.

Extract the invoice information and return ONLY valid JSON.

Use this exact structure:

{
    "document_type": "invoice",
    "invoice_number": null,
    "invoice_date": null,
    "vendor": null,
    "subtotal": null,
    "tax": null,
    "total": null,
    "items": [
        {
            "name": null,
            "quantity": null,
            "unit_price": null,
            "total_price": null
        }
    ]
}

Rules:

1. Identify the document type.
2. Extract the invoice number.
3. Extract the invoice date.
4. Extract the vendor/supplier name.
5. Extract every line item.
6. Extract quantity, unit price and total price for every item.
7. Extract subtotal.
8. Extract tax/GST.
9. Extract final total.
10. If a value cannot be found, use null.
11. Do not invent information.
12. Return ONLY JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            uploaded_file,
            prompt
        ]
    )

    result = response.text

    # Remove markdown code fences if Gemini adds them
    result = result.strip()

    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    return json.loads(result)
