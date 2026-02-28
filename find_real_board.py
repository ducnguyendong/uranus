import fitz
import os

for i in range(10, 50):
    pdf_path = os.path.join(r"D:\Du an dich tan cuc dai toan", f"{i}.pdf")
    if os.path.exists(pdf_path):
        doc = fitz.open(pdf_path)
        page = doc[0]
        images = page.get_images()
        for img in images:
            xref = img[0]
            base = doc.extract_image(xref)
            width, height = base["width"], base["height"]
            if width > 200 and height > 200:
                print(f"Board found on page {i}: {width}x{height}")
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                pix.save(f"real_content_{i}.png")
                doc.close()
                exit()
        doc.close()
