import fitz
doc = fitz.open(r"D:\Du an dich tan cuc dai toan\1.pdf")
text = doc[0].get_text()
print(text)
doc.close()
