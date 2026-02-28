
import fitz
import cv2
import numpy as np

def final_precision_crop(pdf_path, output_path):
    # 1. Render trang ở DPI 400
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom = 400 / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR) if pix.n == 3 else cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)

    # 2. Tiền xử lý: Nhị phân hóa (Otsu)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. Phép dãn (Dilate) để nối các nét bàn cờ và quân cờ thành một khối
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # 4. Tìm các đường bao (Contours)
    cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Bàn cờ là khối lớn nhất nằm ở vùng giữa trang
    page_h, page_w = img.shape[:2]
    board_cnt = None
    max_area = 0
    
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        # Điều kiện lọc: Khối phải đủ lớn và nằm ở khu vực trung tâm (không phải lề)
        if area > max_area and w > page_w * 0.4 and h > page_h * 0.3:
            max_area = area
            board_cnt = (x, y, w, h)

    if board_cnt:
        x, y, w, h = board_cnt
        # Cắt ảnh từ ảnh gốc (không phải ảnh đã dãn)
        # Thêm padding rất nhỏ (2px) để không bị lẹm nét vẽ
        p = 2
        final_board = img[max(0, y-p):min(page_h, y+h+p), max(0, x-p):min(page_w, x+w+p)]
        cv2.imwrite(output_path, final_board)
        return True, (x, y, w, h)
    
    return False, None

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
final_output = r"D:\Du an dich tan cuc dai toan\output\14\board_v4_final.png"

success, coords = final_precision_crop(pdf_file, final_output)
if success:
    print(f"DONE_V4: {coords}")
else:
    print("FAILED_V4")
