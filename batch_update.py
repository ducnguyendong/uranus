import pypdfium2 as pdfium
import os
from PIL import Image

# Convert pages 16 to 25 to HD JPG for processing
pages = range(16, 26)
for p in pages:
    source = f'documents/split_pages/page_{p}.pdf'
    output = f'documents/split_pages/page_{p}_hd.jpg'
    if os.path.exists(source) and not os.path.exists(output):
        pdf = pdfium.PdfDocument(source)
        page = pdf[0]
        bitmap = page.render(scale=3)
        image = bitmap.to_pil()
        image.save(output)
print('Batch conversion update complete.')
