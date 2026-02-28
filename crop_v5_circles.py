
import fitz
import cv2
import numpy as np

def crop_by_pieces(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR) if pix.n == 3 else cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Tìm các quân cờ (hình tròn) bằng HoughCircles
    # minDist=50 (khoảng cách các quân), param1=50, param2=30 (độ nhạy), minRadius=30, maxRadius=100
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=20, maxRadius=80)
    
    # 2. Tìm các đường kẻ bàn cờ
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]
    lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    
    y_min, y_max = 9999, 0
    x_min, x_max = 9999, 0

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center_x, center_y, radius = i
            y_min = min(y_min, center_y - radius)
            y_max = max(y_max, center_y + radius)
            # Không dùng x của quân cờ vì quân cờ nằm lọt thỏm bên trong
            
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x_min = min(x_min, x1, x2)
            x_max = max(x_max, x1, x2)
            # Thêm y của đường kẻ đề phòng không tìm thấy quân cờ
            y_min = min(y_min, y1, y2)
            y_max = max(y_max, y1, y2)

    if x_min < 9999 and y_min < 9999:
        # Padding cực nhỏ (5px) để ảnh không bị bó quá
        p = 5
        res = img[max(0, int(y_min)-p):min(img.shape[0], int(y_max)+p), 
                  max(0, int(x_min)-p):min(img.shape[1], int(x_max)+p)]
        cv2.imwrite(output_path, res)
        return True
    return False

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
output_file = r"D:\Du an dich tan cuc dai toan\output\14\board_v5_circles.png"

if crop_by_pieces(pdf_file, output_file):
    print("DONE_V5")
else:
    print("FAILED_V5")
