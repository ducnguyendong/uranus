import fitz
import os

pdf_path = r"D:\Du an dich tan cuc dai toan\1.pdf"
doc = fitz.open(pdf_path)
page = doc[0]
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Double resolution
pix.save("page_1.png")

# Extract images
for i, img in enumerate(page.get_images(full=True)):
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    with open(f"board_1_{i}.png", "wb") as f:
        f.write(image_bytes)

doc.close()
