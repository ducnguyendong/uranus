import fitz
import os

for i in range(10, 100):
    pdf_name = f"{i}.pdf"
    path = os.path.join(r"D:\Du an dich tan cuc dai toan", pdf_name)
    if os.path.exists(path):
        doc = fitz.open(path)
        if len(doc[0].get_images()) > 0:
            print(f"Found board on page: {i}")
            pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(f"content_page_{i}.png")
            doc.close()
            break
        doc.close()
