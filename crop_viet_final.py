from PIL import Image, ImageDraw, ImageFont
img = Image.open('documents/split_pages/page_14.jpg')
w, h = img.size

# Tọa độ siêu rộng để bảo hiểm [ymin, xmin, ymax, xmax]
# Giảm ymin xuống 530 để phần trên rộng hơn hẳn
left = 120 * w / 1000
top = 530 * h / 1000
right = 520 * w / 1000
bottom = 930 * h / 1000
crop = img.crop((left, top, right, bottom))

# Chỉnh sửa phần chân để Việt hóa
draw = ImageDraw.Draw(crop)
cw, ch = crop.size
# Xóa sạch vùng chứa chữ cũ (图 1)
draw.rectangle([0, ch * 0.82, cw, ch], fill='white')

# Viết lại nhãn tiếng Việt
try:
    # Thử tìm font Arial trên Windows
    font = ImageFont.truetype('arial.ttf', 45)
except:
    font = ImageFont.load_default()

draw.text((cw/2, ch * 0.9), "(Hình 1)", fill='black', font=font, anchor='mm')

crop.save('documents/split_pages/hinh_1_viet_final.jpg')
print('Hinh 1 Viet Final saved.')
