from PIL import Image
img = Image.open('documents/split_pages/page_14.jpg')
w, h = img.size
# Coords from Gemini: [584, 135, 905, 505] -> [ymin, xmin, ymax, xmax]
left = 135 * w / 1000
top = 584 * h / 1000
right = 505 * w / 1000
bottom = 905 * h / 1000
crop = img.crop((left, top, right, bottom))
crop.save('documents/split_pages/hinh_1_extra_wide.jpg')
print('Wide crop saved.')
