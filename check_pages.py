import fitz
doc = fitz.open(r"D:\Du an dich tan cuc dai toan\1.pdf")
print(f"1.pdf pages: {len(doc)}")
doc.close()

doc2 = fitz.open(r"D:\Du an dich tan cuc dai toan\2.pdf")
print(f"2.pdf pages: {len(doc2)}")
if len(doc2) > 0:
    pix = doc2[0].get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save("page_2_1.png")
doc2.close()
