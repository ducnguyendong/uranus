
import fitz
import sys

def check_images(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    img_list = page.get_images(full=True)
    print(f"Page {pdf_path}: {len(img_list)} images found")
    # Xuất ảnh ra để AI nhìn
    for img_index, img in enumerate(img_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        with open(f"temp_page_{img_index}.png", "wb") as f:
            f.write(image_bytes)

check_images(sys.argv[1])
