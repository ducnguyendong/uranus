import fitz
import os

pdf_path = r"D:\Du an dich tan cuc dai toan\10.pdf"
doc = fitz.open(pdf_path)
page = doc[0]

# Save full page as high-res image for OCR/Context
pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
pix.save("page_10_full.png")

# Extract board image
images = page.get_images(full=True)
if images:
    xref = images[0][0]
    base_image = doc.extract_image(xref)
    with open("board_10.png", "wb") as f:
        f.write(base_image["image"])

doc.close()
