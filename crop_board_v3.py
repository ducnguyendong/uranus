
import fitz  # PyMuPDF
import cv2
import numpy as np

def crop_chessboard_precision(pdf_path, output_image_path):
    # 1. Render PDF page to high-res image
    doc = fitz.open(pdf_path)
    page = doc[0]
    zoom = 4  # Tăng lên 4 để cực kỳ sắc nét
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    
    if pix.n == 3:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
    else:
        img = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)

    # 2. Tiền xử lý để tìm lưới bàn cờ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Dùng hình thái học để làm nổi bật các đường thẳng của bàn cờ
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Kết hợp lại để có khung bàn cờ sạch
    cnts_h = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts_v = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # Lấy tọa độ bao phủ tất cả các đường thẳng
    x_coords = []
    y_coords = []

    for c in cnts_h:
        x, y, w, h = cv2.boundingRect(c)
        if w > 200: # Lọc bỏ các vệt nhiễu nhỏ
            y_coords.extend([y, y + h])
            x_coords.extend([x, x + w])
            
    for c in cnts_v:
        x, y, w, h = cv2.boundingRect(c)
        if h > 200: # Lọc bỏ các vệt nhiễu nhỏ
            x_coords.extend([x, x + w])
            y_coords.extend([y, y + h])

    if x_coords and y_coords:
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # Padding vừa đủ để lấy quân Tướng/Soái mà KHÔNG lấy chữ bên dưới
        # Quân cờ thường cao hơn vạch kẻ khoảng 10% chiều cao một ô
        padding_top = 70   # Lấy trọn quân Tướng (将)
        padding_bottom = 65 # Lấy trọn quân Soái (帅)
        padding_side = 10

        y1 = max(0, y_min - padding_top)
        y2 = min(img.shape[0], y_max + padding_bottom)
        x1 = max(0, x_min - padding_side)
        x2 = min(img.shape[1], x_max + padding_side)

        # Cắt và lưu
        board_img = img[y1:y2, x1:x2]
        cv2.imwrite(output_image_path, board_img)
        return True, (x1, y1, x2, y2)
    
    return False, None

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
output_img = r"D:\Du an dich tan cuc dai toan\output\14\board_final_precision.png"

success, coords = crop_chessboard_precision(pdf_file, output_img)
if success:
    print(f"DONE_PRECISION: {coords}")
else:
    print("FAILED_PRECISION")
