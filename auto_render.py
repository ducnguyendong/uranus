import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

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

def render_page(page_num, text_content, board_data):
    canvas_w, canvas_h = 2480, 3508
    canvas = Image.new('RGB', (canvas_w, canvas_h), 'white')
    draw = ImageDraw.Draw(canvas)
    
    try:
        font_bold = ImageFont.truetype('arialbd.ttf', 60)
        font_title = ImageFont.truetype('arialbd.ttf', 100)
        font_regular = ImageFont.truetype('arial.ttf', 55)
        font_label = ImageFont.truetype('arial.ttf', 28)
    except:
        font_bold = font_title = font_regular = font_label = ImageFont.load_default()

    y_offset = 200
    # Tiêu đề tạm cho trang
    draw.text((canvas_w/2, y_offset), f"TRANG {page_num}", fill='black', font=font_title, anchor='mm')
    y_offset += 200

    # Vẽ văn bản dịch
    for block in text_content:
        lines = textwrap.wrap(block, width=70)
        for line in lines:
            draw_styled_text(draw, (200, y_offset), line, font_regular, font_bold)
            y_offset += 80
        y_offset += 40

    # Chèn các bàn cờ
    img_source = Image.open(f'documents/split_pages/page_{page_num}_hd.jpg')
    w, h = img_source.size
    
    for board in board_data:
        # Lấy tọa độ và nới lề theo chuẩn V8
        ymin, xmin, ymax, xmax = board['box']
        label = board['label']
        
        # Cắt sát (nới nhẹ trên dưới)
        left, top, right, bottom = xmin * w / 1000, (ymin-15) * h / 1000, xmax * w / 1000, (ymax+10) * h / 1000
        crop = img_source.crop((left, top, right, bottom))
        
        # Làm sạch và Việt hóa nhãn
        cw, ch = crop.size
        hinh_canvas = Image.new('RGB', (cw, ch + 80), 'white')
        hinh_canvas.paste(crop, (0, 0))
        draw_hinh = ImageDraw.Draw(hinh_canvas)
        draw_hinh.text((cw/2, ch + 40), f"({label})", fill='black', font=font_label, anchor='mm')
        
        # Dán vào trang chính
        disp_w = 800
        disp_h = int(hinh_canvas.size[1] * (disp_w / cw))
        canvas.paste(hinh_canvas.resize((disp_w, disp_h), Image.Resampling.LANCZOS), (200, y_offset))
        y_offset += disp_h + 100

    canvas.save(f'documents/output_v8/page_{page_num}_final.jpg')

# Dữ liệu mẫu trang 15 thu thập được từ Gemini trước đó
text_p15 = [
    "Ví dụ 2: Như (hình 2). Bên Đỏ dùng Binh khống chế Tướng, dùng Sĩ quản lý Tốt mà thắng.",
    "1. Binh 4 bình 5, Tướng 5 thối 1",
    "2. Sĩ 4 tiến 5, Tướng 5 thối 1",
    "3. Binh 5 tiến 1, Tướng 5 bình 4",
    "4. Binh 5 tiến 1... (Đỏ thắng)",
    "Ví dụ 3: Trong tình huống thông thường, chỉ một Sĩ có thể thủ hòa đơn Binh. Như (hình 3) là một trường hợp đặc biệt, Binh và Tướng của bên Đỏ vừa khéo khống chế được Tướng đen, hình thành thế công kẹp hai hướng 'Binh trái Tướng phải', nhờ đó giành chiến thắng."
]
boards_p15 = [
    {"box": [215, 165, 450, 475], "label": "Hình 2"},
    {"box": [620, 165, 850, 475], "label": "Hình 3"}
]

render_page(15, text_p15, boards_p15)
print('Page 15 Rendered.')
