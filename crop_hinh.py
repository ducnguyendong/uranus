import cv2
img = cv2.imread(r'D:/Du an dich tan cuc dai toan/26/page_26_full.png')
# Hình 21: Thường ở phía trên, bên trái
h21 = img[100:650, 150:700]
cv2.imwrite(r'D:/Du an dich tan cuc dai toan/26/hinh_21.png', h21)

# Hình 22: Thường ở phía dưới
h22 = img[1650:1980, 150:700]
cv2.imwrite(r'D:/Du an dich tan cuc dai toan/26/hinh_22.png', h22)
