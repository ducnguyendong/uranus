import pypdfium2 as pdfium
import os
from PIL import Image

source = 'documents/split_pages/page_13.pdf'
output_jpg = 'documents/split_pages/page_13.jpg'

pdf = pdfium.PdfDocument(source)
page = pdf[0]
bitmap = page.render(scale=3) # Higher scale for better OCR/Vision
image = bitmap.to_pil()
image.save(output_jpg)
print(f'Converted {source} to {output_jpg}')
