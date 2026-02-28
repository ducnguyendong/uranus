
import fitz  # PyMuPDF
import cv2
import numpy as np
import os

def crop_chessboard(pdf_path, output_image_path):
    # 1. Mở PDF và chuyển trang thành ảnh chất lượng cao (300 DPI)
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3)) # Phóng đại 3 lần
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    
    if pix.n == 3:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    else:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)

    # 2. Xử lý ảnh
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Tìm các đường thẳng khung bàn cờ
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 150, minLineLength=150, maxLineGap=15)
    
    if lines is not None:
        all_x = []
        all_y = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            all_x.extend([x1, x2])
            all_y.extend([y1, y2])
        
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        
        # Mở rộng vùng cắt để lấy đủ quân Tướng/Soái nhưng chừa chữ Trung Quốc
        padding_v = 45  
        padding_h = 10  
        
        final_x_min = max(0, x_min - padding_h)
        final_y_min = max(0, y_min - padding_v)
        final_x_max = min(img.shape[1], x_max + padding_h)
        final_y_max = min(img.shape[0], y_max + padding_v)
        
        # Cắt ảnh
        board_img = img[final_y_min:final_y_max, final_x_min:final_x_max]
        cv2.imwrite(output_image_path, board_img)
        return True
    return False

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
output_img = r"D:\Du an dich tan cuc dai toan\output\14\board_clean_v2.png"

if crop_chessboard(pdf_file, output_img):
    print("DONE_CROP")
else:
    print("FAILED_CROP")
