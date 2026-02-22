from PIL import Image, ImageDraw, ImageFont
import os

# 1. Setup Canvas (A4 at 300 DPI is approx 2480 x 3508)
# Let's use 150 DPI for a reasonable file size: 1240 x 1754
width, height = 1240, 1754
bg_color = (255, 255, 255)
img = Image.new('RGB', (width, height), bg_color)
draw = ImageDraw.Draw(img)

# 2. Load Fonts (Using Arial or similar if possible, or default)
try:
    font_title = ImageFont.truetype('arial.ttf', 50)
    font_header = ImageFont.truetype('arial.ttf', 30)
    font_body = ImageFont.truetype('arial.ttf', 26)
    font_bold = ImageFont.truetype('arialbd.ttf', 28)
except:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_bold = ImageFont.load_default()

# 3. Content
header_text = "Chương 1: Cờ tàn Tốt đơn giản | 1"
title_text = "CHƯƠNG 1: CỜ TÀN TỐT ĐƠN GIẢN"
intro_text = "Trong các quân tấn công, Tốt có uy lực nhỏ nhất, cách đi đơn giản, sau khi qua sông mới có thể đi ngang. Các thế cờ tàn về Tốt nói chung tương đối đơn giản, dễ nắm bắt. Bây giờ chúng ta bắt đầu tìm hiểu từ Tốt đơn và Tốt đôi."
section_title = "Tiết 1: Các thế Tốt đơn thắng khéo"
section_intro = "Khả năng của Tốt có hạn, Tốt đơn chỉ có thể chiến thắng Tướng đơn độc. Trong những trường hợp đặc biệt, Tốt phối hợp với Tướng, Sĩ, Tượng có thể tạo thành một số thế thắng khéo."
example_title = "Ví dụ 1"
example_intro = "Như (Hình 1), là một thế thắng khéo nhờ sự phối hợp giữa Tốt đơn và Tướng (Đỏ)."
moves_text = [
    "1. Tướng 5 bình 4! ...........",
    "Nước cờ kiềm chế rất hay. Nếu dùng Tốt ăn Sĩ, thì sẽ vừa vặn hình thành cục diện một Sĩ thủ hòa Tốt đơn.",
    "1. ........... Tướng 6 tấn 1",
    "Nếu đổi đi Tướng 6 bình 5, thì Binh 5 bình 6, Sĩ 6 thoái 5, Tướng 6 tấn 1 Đỏ thắng.",
    "2. Binh 5 bình 6 - Tướng 6 bình 5",
    "3. Tướng 4 tấn 1 - Tướng 5 thoái 1",
    "4. Binh 6 tấn 1 - Sĩ 6 thoái 5",
    "5. Tướng 4 bình 5 (Đỏ thắng)"
]

# 4. Drawing
y = 100
draw.text((width//2, y), header_text, fill='black', font=font_header, anchor='mt')
y += 100
draw.text((width//2, y), title_text, fill='black', font=font_title, anchor='mt')
y += 100

def draw_wrapped_text(draw, text, font, x, y, max_width):
    lines = []
    words = text.split()
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    for line in lines:
        draw.text((x, y), line, fill='black', font=font)
        y += font.size + 10
    return y

y = draw_wrapped_text(draw, intro_text, font_body, 100, y, width - 200)
y += 40
draw.text((width//2, y), section_title, fill='black', font=font_bold, anchor='mt')
y += 60
y = draw_wrapped_text(draw, section_intro, font_body, 100, y, width - 200)
y += 40
draw.text((100, y), example_title, fill='black', font=font_bold)
y += 40
y = draw_wrapped_text(draw, example_intro, font_body, 100, y, width - 200)
y += 40

# 5. Insert Image 1
chess_img = Image.open('documents/split_pages/hinh_1_crop.jpg')
# Resize chess image to fit
cw, ch = chess_img.size
target_w = 400
target_h = int(ch * target_w / cw)
chess_img = chess_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
img.paste(chess_img, (100, y))

# 6. Draw Moves next to image
move_x = 100 + target_w + 50
move_y = y
for move in moves_text:
    move_y = draw_wrapped_text(draw, move, font_body, move_x, move_y, width - move_x - 100)
    move_y += 10

# 7. Save
img.save('documents/Tuong_Ky_Trang_1_Hoan_Chinh.pdf')
img.save('documents/Tuong_Ky_Trang_1_Hoan_Chinh.jpg')
print('PDF and JPG created.')
