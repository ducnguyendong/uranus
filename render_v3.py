import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. Load Hình 1 (bản đã cắt đầy đủ từ trang 14)
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
    font_chess_label = ImageFont.truetype('arial.ttf', 45)
except:
    font_bold = font_title = font_regular = font_chess_label = ImageFont.load_default()

def draw_styled_text(draw, pos, text, font_reg, font_bold, fill='black'):
    x, y = pos
    keywords = ['Tướng', 'Binh', 'Sĩ', 'Tượng', 'Pháo', 'Xe', 'Soái', 'Tốt']
    words = text.split(' ')
    current_x = x
    for word in words:
        clean_word = word.strip('.,()!')
        is_keyword = any(k.lower() == clean_word.lower() for k in keywords)
        active_font = font_bold if is_keyword else font_reg
        draw.text((current_x, y), word + ' ', fill=fill, font=active_font)
        bbox = draw.textbbox((current_x, y), word + ' ', font=active_font)
        current_x += (bbox[2] - bbox[0])

# 3. Xử lý Việt hóa nhãn bàn cờ MỘT CÁCH AN TOÀN (mở rộng canvas hình thay vì cắt bớt)
hinh_1_w, hinh_1_h = hinh_1.size
# Tạo một hình mới cao hơn một chút để chứa nhãn mới mà không đè lên đường biên cũ
new_hinh_h = int(hinh_1_h * 1.1) 
hinh_1_viet = Image.new('RGB', (hinh_1_w, new_hinh_h), 'white')
# Dán hình gốc vào (chỉ lấy phần trên, bỏ phần chữ Tàu ở đáy)
hinh_1_viet.paste(hinh_1.crop((0, 0, hinh_1_w, int(hinh_1_h * 0.88))), (0, 0))

draw_hinh = ImageDraw.Draw(hinh_1_viet)
# Viết nhãn "(Hình 1)" ở khoảng trống mới tạo ra
draw_hinh.text((hinh_1_w/2, new_hinh_h - 40), "(Hình 1)", fill='black', font=font_chess_label, anchor='mm')

# 4. Vẽ văn bản trang chính
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

y_offset += 180 

# 5. Chèn hình đã sửa (giữ kích thước hiển thị tốt)
display_w = 850
display_h = int(new_hinh_h * (display_w / hinh_1_w))
hinh_1_final = hinh_1_viet.resize((display_w, display_h), Image.Resampling.LANCZOS)
canvas.paste(hinh_1_final, (200, y_offset))

# 6. Vẽ nước đi bên cạnh
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

# 7. Lưu kết quả
canvas.save('documents/Tuong_Ky_Trang_1_Chuan_V3.jpg')
print('Render V3 complete.')
