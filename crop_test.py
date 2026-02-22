from PIL import Image
img = Image.open('documents/split_pages/page_16.jpg')
w, h = img.size
# Coords from Gemini: [215, 165, 454, 475] -> [ymin, xmin, ymax, xmax]
left = 165 * w / 1000
top = 215 * h / 1000
right = 475 * w / 1000
bottom = 454 * h / 1000
crop = img.crop((left, top, right, bottom))
crop.save('documents/split_pages/hinh_1_crop.jpg')
print('Crop saved.')
