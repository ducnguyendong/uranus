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

def render_page_v8(page_num, text_blocks, board_data):
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
    draw.text((canvas_w/2, y_offset), f"TRANG {page_num}", fill='black', font=font_title, anchor='mm')
    y_offset += 250

    img_source = Image.open(f'documents/split_pages/page_{page_num}_hd.jpg')
    w, h = img_source.size
    
    current_board_idx = 0
    
    for block in text_blocks:
        # Check if block is a trigger for a board
        board_trigger = False
        if current_board_idx < len(board_data):
            label = board_data[current_board_idx]['label']
            if f'({label})' in block:
                board_trigger = True
        
        # Wrap text
        max_w = 70 if not board_trigger else 35
        lines = textwrap.wrap(block, width=80)
        
        for line in lines:
            draw_styled_text(draw, (200, y_offset), line, font_regular, font_bold)
            y_offset += 85
            
        if board_trigger:
            y_offset += 100
            board = board_data[current_board_idx]
            ymin, xmin, ymax, xmax = board['box']
            # Crop with V8 safety margins
            left, top, right, bottom = xmin * w / 1000, (ymin-15) * h / 1000, xmax * w / 1000, (ymax+10) * h / 1000
            crop = img_source.crop((left, top, right, bottom))
            
            cw, ch = crop.size
            # Add label
            hinh_canvas = Image.new('RGB', (cw, ch + 100), 'white')
            hinh_canvas.paste(crop, (0, 0))
            draw_hinh = ImageDraw.Draw(hinh_canvas)
            draw_hinh.text((cw/2, ch + 50), f"({board['label']})", fill='black', font=font_label, anchor='mm')
            
            # Resize and paste
            disp_w = 850
            disp_h = int(hinh_canvas.size[1] * (disp_w / cw))
            canvas.paste(hinh_canvas.resize((disp_w, disp_h), Image.Resampling.LANCZOS), (200, y_offset))
            y_offset += disp_h + 150
            current_board_idx += 1
        else:
            y_offset += 40

    canvas.save(f'documents/output_v8/page_{page_num}_final.jpg')

# --- Page 16 Data ---
text_16 = [
    "Chương I: Các tàn cuộc Binh đơn giản",
    "Ví dụ 4: Như (Hình 4) là một ván thắng nhờ sự trợ công của Tượng, quân Tượng này ngoài tác dụng che mặt Tướng, còn có thể hỗ trợ Binh đỏ khống chế Tướng đen.",
    "1. Tướng 5 tấn 1! ........... Đây là một nước chờ cần thiết, khiến bên Đen không thể ứng phó. Cần tránh: Tượng 5 tấn 3, Sĩ 5 thoái 4, Tướng 5 bình 4, Sĩ 4 tấn 5, Tướng 4 bình 5, Sĩ 5 thoái 4, Tướng 5 tấn 1, Tướng 5 bình 6, Binh 5 bình 4, Sĩ 4 tấn 5, Binh 4 bình 5, Sĩ 5 thoái 4, hòa cờ.",
    "1.........Sĩ 5 thoái 6  2.Binh 5 bình 6, Tướng 5 tấn 1. Nếu đổi đi Tướng 5 bình 4, Tướng 5 bình 6, Sĩ 6 tấn 5, Binh 6 tấn 1, Tướng 4 bình 5, Tướng 6 bình 5, Sĩ 5 thoái 4, Tướng 5 bình 4, Sĩ 4 tấn 5, Tượng 5 tấn 3, Sĩ 5 thoái 4, Tướng 4 tấn 1, Sĩ 4 tấn 5, Tướng 4 bình 5 Đỏ thắng.",
    "3.Tướng 5 bình 4, Tướng 5 thoái 1  4.Binh 6 tấn 1, Sĩ 6 tấn 5  5.Tượng 5 tấn 3, Sĩ 5 thoái 6  6.Tướng 4 tấn 1, Sĩ 6 tấn 5  7.Tướng 4 bình 5, Tướng 5 bình 6  8.Binh 6 bình 5 (Đỏ thắng)",
    "Tiết 2: Các thế hòa lệ của đơn Binh. Một số cục diện tất yếu dẫn đến kết quả hòa, mang ý nghĩa điển hình, được gọi là tàn cuộc 'hòa lệ'. Nên học tập và nắm vững các loại hình hòa lệ khác nhau, đây là kiến thức phổ thông cần thiết cho người chơi cờ. Dưới đây xin nêu ví dụ bàn về các thế hòa lệ của đơn Binh."
]
boards_16 = [{"box": [218, 164, 454, 474], "label": "Hình 4"}]
render_page_v8(16, text_16, boards_16)

# --- Page 17 Data ---
text_17 = [
    "Ví dụ 1: Như (Hình 5), đây là thế cờ một Sĩ thủ hòa đơn Binh. Chỉ cần chú ý không để Binh đỏ khống chế Tướng đen, một quân Sĩ đen là đủ để chống đỡ cuộc tấn công của đơn Binh bên đỏ.",
    "1. Binh 5 tiến 1  Sĩ 5 thoái 6. Nếu đổi đi Tướng 4 bình 5? Tướng 4 bình 5. Sĩ 5 thoái 6, Binh 5 bình 6, Tướng 5 bình 4, Tướng 5 bình 6, đỏ thắng.",
    "2. Tướng 4 bình 5  Tướng 4 tiến 1. 3. Sĩ 5 thoái 4  Tướng 4 thoái 1. 4. Binh 5 bình 6  Sĩ 6 tiến 5. 5. Binh 6 bình 5  Sĩ 5 thoái 6. 6. Tướng 5 tiến 1  Tướng 4 tiến 1. (Hòa cờ)",
    "Ví dụ 2: Như (Hình 6), Binh đỏ có thể đi nước chờ, chỉ cần chú ý tác dụng 'xích chân' của Tướng đỏ đối với quân Tốt và Tướng bên đen, khiến Tướng đen không thể phát huy uy lực của trung Tướng, là có thể thủ hòa.",
    "1. Binh 8 bình 7  Tướng 5 bình 4. 2. Tướng 5 bình 4  Tốt 5 bình 6. 3. Tướng 4 bình 5!  ........... Tướng đỏ nhất định phải kịp thời chiếm lĩnh lộ giữa, mới có thể thủ hòa.",
    "3 ........... Tốt 6 bình 5. 4. Tướng 5 bình 4  Tướng 4 bình 5. 5. Tướng 4 bình 5  (Hòa cờ)"
]
boards_17 = [
    {"box": [255, 170, 505, 485], "label": "Hình 5"},
    {"box": [605, 170, 850, 485], "label": "Hình 6"}
]
render_page_v8(17, text_17, boards_17)

print('Rendered pages 16 and 17.')
