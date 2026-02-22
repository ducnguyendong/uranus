import pypdfium2 as pdfium
import os

source = 'documents/split_pages/page_16.pdf'
output = 'documents/split_pages/page_16.jpg'

pdf = pdfium.PdfDocument(source)
page = pdf[0]
bitmap = page.render(scale=2)
image = bitmap.to_pil()
image.save(output)
print(f'Converted {source} to {output}')
