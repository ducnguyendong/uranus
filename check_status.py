
import os
import json

base_path = r"D:\Du an dich tan cuc dai toan"
results = []

for p in range(14, 41):
    folder = os.path.join(base_path, str(p))
    if not os.path.exists(folder):
        results.append(f"{p}: MISSING_FOLDER")
        continue
    
    files = os.listdir(folder)
    has_json = "content.json" in files
    has_full = f"page_{p}_full.png" in files
    has_docx = any(f.endswith(".docx") for f in files)
    
    status = []
    if has_json: status.append("JSON")
    if has_full: status.append("FULL")
    if has_docx: status.append("DOCX")
    
    results.append(f"{p}: {', '.join(status)}")

print("\n".join(results))
