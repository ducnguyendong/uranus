
import fitz
import sys

def get_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    # Vì là PDF scan, get_text() có thể rỗng, thử lấy blocks
    blocks = doc[0].get_text("blocks")
    for b in blocks:
        print(b[4]) # In nội dung text trong block

get_text_blocks(sys.argv[1])
