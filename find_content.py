import fitz
import os

for i in range(3, 10):
    pdf_name = f"{i}.pdf"
    path = os.path.join(r"D:\Du an dich tan cuc dai toan", pdf_name)
    if os.path.exists(path):
        doc = fitz.open(path)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(1, 1))
        pix.save(f"check_page_{i}.png")
        doc.close()
