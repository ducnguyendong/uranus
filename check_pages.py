import pypdfium2 as pdfium
import os
from PIL import Image

for i in range(1, 16):
    source = f'documents/split_pages/page_{i}.pdf'
    output = f'documents/split_pages/page_{i}.jpg'
    if os.path.exists(source):
        pdf = pdfium.PdfDocument(source)
        page = pdf[0]
        bitmap = page.render(scale=1) # Low res for quick check
        image = bitmap.to_pil()
        image.save(output)
print('Pages 1-15 converted.')
