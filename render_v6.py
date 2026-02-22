from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. Tinh chỉnh Hình 1 V6: Rộng hơn về bên phải
img_source = Image.open('documents/split_pages/page_14.jpg')
w, h = img_source.size

# Tọa độ nới rộng hơn về bên phải (right từ 480 lên 520)
# ymin, xmin, ymax, xmax (0-1000)
left, top, right, bottom = 135 * w / 1000, 580 * h / 1000, 520 * w / 1000, 860 * h / 1000
crop = img_source.crop((left, top, right, bottom))

cw, ch = crop.size
draw_crop = ImageDraw.Draw(crop)

# Xóa các thành phần thừa ở vùng nới rộng (phía bên phải và trên)
# Xóa lề phải rộng hơn chút (khoảng 15% chiều rộng crop mới)
draw_crop.rectangle([cw * 0.85, 0, cw, ch], fill='white') 
# Xóa lề trên
draw_crop.rectangle([0, 0, cw, ch * 0.05], fill='white')

# Nới lề dưới rộng rãi như V5
padding_bottom = 80
hinh_1_final_w = cw
hinh_1_final_h = ch + padding_bottom
hinh_1_canvas = Image.new('RGB', (hinh_1_final_w, hinh_1_final_h), 'white')
hinh_1_canvas.paste(crop, (0, 0))

draw_final_hinh = ImageDraw.Draw(hinh_1_canvas)
try:
    font_label = ImageFont.truetype('arial.ttf', 28)
except:
    font_label = ImageFont.load_default()

# Đặt nhãn (Hình 1)
draw_final_hinh.text((hinh_1_final_w/2, hinh_1_final_h - 40), "(Hình 1)", fill='black', font=font_label, anchor='mm')
hinh_1_canvas.save('documents/split_pages/hinh_1_v6_wide.jpg')

# 2. Render trang hoàn chỉnh V6
canvas_w, canvas_h = 2480, 3508
canvas = Image.new('RGB', (canvas_w, canvas_h), 'white')
draw = ImageDraw.Draw(canvas)

try:
    font_bold = ImageFont.truetype('arialbd.ttf', 60)
    font_title = ImageFont.truetype('arialbd.ttf', 100)
    font_regular = ImageFont.truetype('arial.ttf', 55)
except:
    font_bold = font_title = font_regular = ImageFont.load_default()

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

# Vẽ văn bản
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
draw.text((200, y_offset), "Ví dụ 1:", fill='black', font=font_bold)
y_offset += 100
draw_styled_text(draw, (200, y_offset), "Như (Hình 1), là ví dụ Đơn Binh phối hợp với Tướng khéo thắng.", font_regular, font_bold)

y_offset += 200 

# Chèn bàn cờ V6
h1v6 = Image.open('documents/split_pages/hinh_1_v6_wide.jpg')
h1w, h1h = h1v6.size
disp_w = 900 # Tăng độ rộng hiển thị một chút cho cân đối
disp_h = int(h1h * (disp_w / h1w))
canvas.paste(h1v6.resize((disp_w, disp_h), Image.Resampling.LANCZOS), (200, y_offset))

# Vẽ nước đi bên cạnh
x_moves = 1200 # Dịch nước đi sang phải thêm chút do bàn cờ rộng hơn
y_moves = y_offset + 30
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
    draw_styled_text(draw, (x_moves, y_moves), move, font_regular, font_bold)
    y_moves += 90

canvas.save('documents/Tuong_Ky_Trang_1_Hoan_Hao_V6.jpg')
print('Render V6 complete.')
