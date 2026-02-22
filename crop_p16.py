from PIL import Image
img = Image.open('documents/split_pages/page_16.jpg')
w, h = img.size
# Coords for Hình 4: [217, 163, 455, 474]
left = 163 * w / 1000
top = 217 * h / 1000
right = 474 * w / 1000
bottom = 455 * h / 1000
crop = img.crop((left, top, right, bottom))
crop.save('documents/split_pages/hinh_4_crop.jpg')
print('Hình 4 saved.')
