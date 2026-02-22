import pypdfium2 as pdfium
import os
from PIL import Image

# Let's check page 15, 16, 17 to find the actual beginning of Chapter 1
# Based on the user's manual summary earlier, Chapter 1 should be near the start.
# Page 1 (cover), Page 12 (Table of contents), Page 13 (Table of contents)
# Let's try page 16 again (where I found Hình 1 earlier)

source = 'documents/split_pages/page_16.pdf'
output_jpg = 'documents/split_pages/page_16.jpg'

pdf = pdfium.PdfDocument(source)
page = pdf[0]
bitmap = page.render(scale=3)
image = bitmap.to_pil()
image.save(output_jpg)
print(f'Converted {source} to {output_jpg}')
