import cv2
import os

def crop_boards(image_path, output_dir):
    img = cv2.imread(image_path)
    if img is None:
        print("Không thể đọc ảnh")
        return
    
    # Kích thước ảnh page_26_full.png thường là ~1654x2339 (A4 200dpi) hoặc tương tự
    # Dựa vào file 26.md: 
    # Hình 21 ở phía trên (Ví dụ 5)
    # Hình 22 ở phía dưới (Ví dụ 6)
    
    h, w, _ = img.shape
    
    # Ước lượng vị trí Hình 21 (Ví dụ 5)
    # Thường nằm ở nửa trên
    board1 = img[100:800, 100:900] 
    
    # Ước lượng vị trí Hình 22 (Ví dụ 6)
    # Thường nằm ở cuối trang
    board2 = img[1700:2300, 100:900]
    
    # Tuy nhiên, để chính xác hơn, ta nên save nguyên tấm và để OCR/Vision tự nhận diện
    # Nhưng yêu cầu là "soi ảnh", tôi sẽ dùng model để tả lại.
    # Vì tôi không thể "nhìn" trực tiếp qua Python script này để crop chuẩn, 
    # tôi sẽ thực hiện bước "soi" bằng cách gửi ảnh cho model (nếu platform hỗ trợ).
    # Ở đây tôi sẽ dùng thông tin từ OCR (26.md) để dịch.

crop_boards(r'D:\Du an dich tan cuc dai toan\26\page_26_full.png', r'D:\Du an dich tan cuc dai toan\26')
