import pypdfium2 as pdfium
import os
from PIL import Image, ImageDraw, ImageFont

# 1. Chuyển đổi trang 14 (Chương 1 trang 1) sang ảnh chất lượng cao
source_pdf = 'documents/split_pages/page_14.pdf'
page_img_path = 'documents/split_pages/page_14_high.jpg'
pdf = pdfium.PdfDocument(source_pdf)
page = pdf[0]
bitmap = page.render(scale=4) # Tăng scale lên 4 để cực kỳ sắc nét
image = bitmap.to_pil()
image.save(page_img_path)

# 2. Cắt Hình 1 (sử dụng tọa độ chuẩn đã xác nhận)
w, h = image.size
left, top, right, bottom = 164 * w / 1000, 607 * h / 1000, 475 * w / 1000, 878 * h / 1000
hinh_1 = image.crop((left, top, right, bottom))
hinh_1.save('documents/split_pages/hinh_1_final.jpg')

# 3. Tạo trang dịch hoàn chỉnh (Canvas trắng)
canvas_w, canvas_h = 2480, 3508 # A4 tại 300 DPI
canvas = Image.new('RGB', (canvas_w, canvas_h), 'white')
draw = ImageDraw.Draw(canvas)

# Tải font (Sử dụng Arial có sẵn trên Windows)
try:
    font_bold = ImageFont.truetype('arialbd.ttf', 80)
    font_title = ImageFont.truetype('arialbd.ttf', 100)
    font_regular = ImageFont.truetype('arial.ttf', 50)
    font_italic = ImageFont.truetype('ariali.ttf', 50)
except:
    font_bold = font_title = font_regular = font_italic = ImageFont.load_default()

# 4. Vẽ văn bản dịch
y_offset = 200
draw.text((canvas_w/2, y_offset), "CHƯƠNG 1: TÀN CUỘC LOẠI BINH ĐƠN GIẢN", fill='black', font=font_title, anchor='mm')
y_offset += 200

intro_text = "Trong các quân tấn công, Binh có uy lực nhỏ nhất, cách đi đơn giản, sau khi qua sông mới có thể đi ngang. Tàn cuộc loại Binh nhìn chung tương đối đơn giản, dễ nắm bắt. Nay bắt đầu bàn từ Đơn Binh và Song Binh."
import textwrap
lines = textwrap.wrap(intro_text, width=80)
for line in lines:
    draw.text((200, y_offset), line, fill='black', font=font_regular)
    y_offset += 70

y_offset += 100
draw.text((canvas_w/2, y_offset), "TIẾT 1: ĐƠN BINH KHẾO THẮNG", fill='black', font=font_bold, anchor='mm')
y_offset += 150

detail_text = "Năng lực của Binh có hạn, Đơn Binh chỉ có thể thắng tướng đơn độc. Trong những tình huống đặc biệt, Binh phối hợp với Tướng, Sĩ, Tượng có thể tạo thành một số cục diện khéo thắng."
lines = textwrap.wrap(detail_text, width=80)
for line in lines:
    draw.text((200, y_offset), line, fill='black', font=font_regular)
    y_offset += 70

y_offset += 100
draw.text((200, y_offset), "Ví dụ 1:", fill='black', font=font_bold)
y_offset += 100
draw.text((200, y_offset), "Như (Hình 1), là ví dụ Đơn Binh phối hợp với Tướng khéo thắng.", fill='black', font=font_regular)

# 5. Chèn Hình 1
# Resize hình 1 cho phù hợp với trang A4
hinh_1_w, hinh_1_h = hinh_1.size
new_w = 800
new_h = int(hinh_1_h * (new_w / hinh_1_w))
hinh_1_resized = hinh_1.resize((new_w, new_h), Image.Resampling.LANCZOS)
canvas.paste(hinh_1_resized, (200, y_offset + 50))

# 6. Viết tiếp các nước đi bên cạnh hình
x_moves = 1100
y_moves = y_offset + 50
moves = [
    "1. Tướng 5 bình 4!",
    "(Nước cờ kiềm chế rất hay)",
    "    ... Tướng 6 tiến 1",
    "2. Binh 5 bình 6 - Tướng 6 bình 5",
    "3. Tướng 4 tiến 1 - Tướng 5 thoái 1",
    "4. Binh 6 tiến 1 - Sĩ 6 thoái 5",
    "5. Tướng 4 bình 5 (Đỏ thắng)"
]
for move in moves:
    draw.text((x_moves, y_moves), move, fill='black', font=font_regular)
    y_moves += 80

# 7. Lưu kết quả
canvas.save('documents/Tuong_Ky_Trang_1_Hoan_Chinh.jpg')
