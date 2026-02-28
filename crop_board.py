
import fitz  # PyMuPDF
import cv2
import numpy as np
import os

def crop_chessboard(pdf_path, output_image_path):
    # 1. Mở PDF và chuyển trang thành ảnh chất lượng cao (300 DPI)
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3)) # Phóng đại 3 lần để rõ nét
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    
    # Chuyển sang BGR cho OpenCV
    if pix.n == 3:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    else:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)

    # 2. Xử lý ảnh để tìm bàn cờ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Dùng Canny để tìm cạnh
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Tìm các đường thẳng (HoughLinesP)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        all_x = []
        all_y = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            all_x.extend([x1, x2])
            all_y.extend([y1, y2])
        
        # Lấy vùng bao quanh các đường thẳng (thường là khung bàn cờ)
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        
        # Thêm một chút padding
        padding = 10
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(img.shape[1], x_max + padding)
        y_max = min(img.shape[0], y_max + padding)
        
        # Cắt ảnh
        board_img = img[y_min:y_max, x_min:x_max]
        
        # Lưu ảnh
        cv2.imwrite(output_image_path, board_img)
        return True, (x_min, y_min, x_max, y_max)
    return False, None

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
output_img = r"D:\Du an dich tan cuc dai toan\output\14\board_clean.png"

success, coords = crop_chessboard(pdf_file, output_img)
if success:
    print(f"SUCCESS: Đã cắt bàn cờ tại {coords}")
else:
    print("FAILED: Không tìm thấy bàn cờ.")
