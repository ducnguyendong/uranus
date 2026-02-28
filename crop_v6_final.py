
import fitz
import cv2
import numpy as np

def final_surgical_crop(pdf_path, output_path):
    # 1. Render trang ở DPI 300
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR) if pix.n == 3 else cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Nhị phân hóa và loại bỏ nhiễu nhỏ
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # 3. Tìm các khối (Contours)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Bàn cờ trong trang này là một khối có diện tích cực lớn, tỷ lệ gần vuông
    best_box = None
    max_area = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = float(w)/h
        
        # Tiêu chuẩn: Diện tích lớn, tỷ lệ rộng/cao khoảng 0.7 - 1.2
        if area > 100000 and 0.7 < aspect_ratio < 1.3:
            if area > max_area:
                max_area = area
                best_box = (x, y, w, h)
    
    if best_box:
        x, y, w, h = best_box
        # Cắt sát mép (không dùng padding vì Contours đã ôm trọn cả quân cờ lồi ra)
        res = img[y:y+h, x:x+w]
        cv2.imwrite(output_path, res)
        return True
    return False

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
output_file = r"D:\Du an dich tan cuc dai toan\output\14\board_v6_final.png"

if final_surgical_crop(pdf_file, output_file):
    print("DONE_V6")
else:
    print("FAILED_V6")
