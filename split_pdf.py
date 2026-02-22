import pypdf
import os

source = 'documents/Tuong_Ky_Tan_Cuoc_Dai_Toan_GOC.pdf'
output_dir = 'documents/split_pages'

reader = pypdf.PdfReader(source)
total_pages = len(reader.pages)

for i in range(total_pages):
    writer = pypdf.PdfWriter()
    writer.add_page(reader.pages[i])
    with open(f'{output_dir}/page_{i+1}.pdf', 'wb') as f:
        writer.write(f)
print(f'Done splitting {total_pages} pages.')
