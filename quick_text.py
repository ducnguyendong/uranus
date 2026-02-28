
import fitz
import sys

def get_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = doc[0].get_text()
    print(text)

get_text(sys.argv[1])
