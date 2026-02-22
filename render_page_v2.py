import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. Load Hình 1 final đã cắt chuẩn
hinh_1 = Image.open('documents/split_pages/hinh_1_final.jpg')

# 2. Tạo trang canvas A4 (300 DPI)
canvas_w, canvas_h = 2480, 3508
canvas = Image.new('RGB', (canvas_w, canvas_h), 'white')
draw = ImageDraw.Draw(canvas)

# Tải font
try:
    font_bold = ImageFont.truetype('arialbd.ttf', 60)
    font_title = ImageFont.truetype('arialbd.ttf', 100)
    font_regular = ImageFont.truetype('arial.ttf', 55)
    font_italic = ImageFont.truetype('ariali.ttf', 50)
except:
    font_bold = font_title = font_regular = font_italic = ImageFont.load_default()

def draw_styled_text(draw, pos, text, font_reg, font_bold, fill='black'):
    x, y = pos
    keywords = ['Tướng', 'Binh', 'Sĩ', 'Tượng', 'Pháo', 'Xe', 'Soái', 'Tốt']
    words = text.split(' ')
    current_x = x
    for word in words:
        # Xử lý các dấu câu dính liền để nhận diện keyword
        clean_word = word.strip('.,()!')
        is_keyword = any(k.lower() == clean_word.lower() for k in keywords)
        active_font = font_bold if is_keyword else font_reg
        draw.text((current_x, y), word + ' ', fill=fill, font=active_font)
        # Tịnh tiến x
        bbox = draw.textbbox((current_x, y), word + ' ', font=active_font)
        current_x += (bbox[2] - bbox[0])

# 3. Vẽ văn bản
y_offset = 200
draw.text((canvas_w/2, y_offset), "CHƯƠNG 1: TÀN CUỘC LOẠI BINH ĐƠN GIẢN", fill='black', font=font_title, anchor='mm')
y_offset += 250

intro_text = "Trong các quân tấn công, Binh có uy lực nhỏ nhất, cách đi đơn giản, sau khi qua sông mới có thể đi ngang. Tàn cuộc loại Binh nhìn chung tương đối đơn giản, dễ nắm bắt. Nay bắt đầu bàn từ Đơn Binh và Song Binh."
lines = textwrap.wrap(intro_text, width=70)
for line in lines:
    draw_styled_text(draw, (200, y_offset), line, font_regular, font_bold)
    y_offset += 80

y_offset += 120
draw.text((canvas_w/2, y_offset), "TIẾT 1: ĐƠN BINH KHẾO THẮNG", fill='black', font=font_bold, anchor='mm')
y_offset += 150

detail_text = "Năng lực của Binh có hạn, Đơn Binh chỉ có thể thắng Tướng đơn độc. Trong những tình huống đặc biệt, Binh phối hợp với Tướng, Sĩ, Tượng có thể tạo thành một số cục diện khéo thắng."
lines = textwrap.wrap(detail_text, width=70)
for line in lines:
    draw_styled_text(draw, (200, y_offset), line, font_regular, font_bold)
    y_offset += 80

y_offset += 100
draw_styled_text(draw, (200, y_offset), "Ví dụ 1:", font_regular, font_bold)
y_offset += 100
draw_styled_text(draw, (200, y_offset), "Như (Hình 1), là ví dụ Đơn Binh phối hợp với Tướng khéo thắng.", font_regular, font_bold)

# Dịch chuyển bàn cờ xuống dưới thêm 1 dòng (~100px)
y_offset += 200 

# 4. Chèn Hình 1
hinh_1_w, hinh_1_h = hinh_1.size
new_w = 850
new_h = int(hinh_1_h * (new_w / hinh_1_w))
hinh_1_resized = hinh_1.resize((new_w, new_h), Image.Resampling.LANCZOS)
canvas.paste(hinh_1_resized, (200, y_offset))

# 5. Vẽ nước đi bên cạnh
x_moves = 1150
y_moves = y_offset
moves_styled = [
    "1. Tướng 5 bình 4!",
    "(Nước cờ kiềm chế rất hay)",
    "    ... Tướng 6 tiến 1",
    "2. Binh 5 bình 6 - Tướng 6 bình 5",
    "3. Tướng 4 tiến 1 - Tướng 5 thoái 1",
    "4. Binh 6 tiến 1 - Sĩ 6 thoái 5",
    "5. Tướng 4 bình 5 (Đỏ thắng)"
]
for move in moves_styled:
    draw_styled_text(draw, (x_moves, y_moves), move, font_regular, font_bold)
    y_moves += 90

# 6. Lưu kết quả
canvas.save('documents/Tuong_Ky_Trang_1_Hoan_Chinh_V2.jpg')
print('Render V2 complete.')
