import fitz
pdf_path = r"D:\Du an dich tan cuc dai toan\2.pdf"
doc = fitz.open(pdf_path)
page = doc[0]
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
pix.save("page_2.png")
doc.close()
