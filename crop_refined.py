from PIL import Image, ImageDraw, ImageFont
img = Image.open('documents/split_pages/page_14.jpg')
w, h = img.size

# Giữ nguyên tọa độ siêu rộng an toàn
left = 120 * w / 1000
top = 530 * h / 1000
right = 520 * w / 1000
bottom = 930 * h / 1000
crop = img.crop((left, top, right, bottom))

draw = ImageDraw.Draw(crop)
cw, ch = crop.size
# Xóa vùng chữ cũ
draw.rectangle([0, ch * 0.82, cw, ch], fill='white')

# Sử dụng font size nhỏ hơn (30-35) để tương đồng với văn bản chính
try:
    font = ImageFont.truetype('arial.ttf', 35)
except:
    font = ImageFont.load_default()

# Viết lại nhãn "(Hình 1)" với kích thước nhỏ hơn
draw.text((cw/2, ch * 0.88), "(Hình 1)", fill='black', font=font, anchor='mm')

crop.save('documents/split_pages/hinh_1_viet_refined.jpg')
print('Hinh 1 refined saved.')
