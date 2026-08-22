from services.gemini_service import analyze_invoice


file_path = "uploads/sample_invoice.png"

result = analyze_invoice(file_path)

print("\n========== DOCUMENT AI RESULT ==========\n")

print(result)

print("\n=========================================\n")
