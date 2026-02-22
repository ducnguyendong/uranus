import pypdfium2 as pdfium
import os
from PIL import Image

pages = range(15, 26)
for p in pages:
    source = f'documents/split_pages/page_{p}.pdf'
    output = f'documents/split_pages/page_{p}_hd.jpg'
    if os.path.exists(source):
        pdf = pdfium.PdfDocument(source)
        page = pdf[0]
        bitmap = page.render(scale=3)
        image = bitmap.to_pil()
        image.save(output)
print('Pages 15-25 converted to HD.')
