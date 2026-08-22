from services.gemini_service import analyze_purchase_order


file_path = "uploads/sample_po.png"


result = analyze_purchase_order(file_path)


print("\n========== PURCHASE ORDER ==========\n")

print(result)

print("\n====================================\n")
