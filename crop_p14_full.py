from PIL import Image
img = Image.open('documents/split_pages/page_14.jpg')
w, h = img.size
# Coords from Gemini: [607, 164, 878, 475]
left = 164 * w / 1000
top = 607 * h / 1000
right = 475 * w / 1000
bottom = 878 * h / 1000
crop = img.crop((left, top, right, bottom))
crop.save('documents/split_pages/hinh_1_full.jpg')
print('Hình 1 full saved.')
