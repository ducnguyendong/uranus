import pypdfium2 as pdfium
import os
from PIL import Image

# Let's check page 14 (likely the actual start of Chapter 1)
source = 'documents/split_pages/page_14.pdf'
output_jpg = 'documents/split_pages/page_14.jpg'

pdf = pdfium.PdfDocument(source)
page = pdf[0]
bitmap = page.render(scale=3)
image = bitmap.to_pil()
image.save(output_jpg)
print(f'Converted {source} to {output_jpg}')
