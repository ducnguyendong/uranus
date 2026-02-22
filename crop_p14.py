from PIL import Image
img = Image.open('documents/split_pages/page_14.jpg')
w, h = img.size
# Coords for Hình 1: [611, 164, 843, 473]
left = 164 * w / 1000
top = 611 * h / 1000
right = 473 * w / 1000
bottom = 843 * h / 1000
crop = img.crop((left, top, right, bottom))
crop.save('documents/split_pages/hinh_1_crop.jpg')
print('Hình 1 saved.')
