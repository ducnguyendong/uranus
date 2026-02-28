import fitz
import os

for i in range(15, 40, 5):
    path = os.path.join(r"D:\Du an dich tan cuc dai toan", f"{i}.pdf")
    if os.path.exists(path):
        doc = fitz.open(path)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(1, 1))
        pix.save(f"check_content_{i}.png")
        doc.close()
