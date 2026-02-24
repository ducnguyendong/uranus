# QUY TRÌNH DỊCH SÁCH CỜ TƯỚNG (URANUS ❄️)

Quy trình này được thiết lập để tự động hóa việc dịch và dàn trang sách cờ tướng từ PDF (Trung Quốc) sang Word (Việt Nam).

## 1. Các bước thực hiện (Workflow)

### Bước 1: Trích xuất ảnh (Extract)
- Sử dụng thư viện `PyMuPDF` để chuyển đổi trang PDF cụ thể thành file ảnh PNG với độ phân giải cao (300 DPI).
- Đảm bảo hình ảnh sắc nét để phục vụ OCR và cắt hình bàn cờ.

### Bước 2: Cắt hình bàn cờ (Auto-Crop)
- Sử dụng `OpenCV` để nhận diện các đường kẻ và vùng bao của bàn cờ.
- Tự động cắt và lưu thành file ảnh riêng (ví dụ: `board_XX.png`).

### Bước 3: Nhận diện và Dịch thuật (OCR & Translate)
- Sử dụng mô hình AI (Vision) để đọc văn bản tiếng Trung.
- Dịch sang tiếng Việt theo văn phong chuyên môn cờ tướng:
    - Thay "Binh" bằng **Chốt**.
    - Sử dụng thuật ngữ: khéo thắng, Tướng đơn độc, kiềm chế, xỏ xâu...
    - Nước đi: **Đỏ** bình/tiến/thoái ... **Đen** bình/tiến/thoái (nằm trên cùng 1 dòng).

### Bước 4: Tạo file Word (Formatting)
- Sử dụng `python-docx` để dựng lại trang với bố cục:
    - **Font chữ:** Times New Roman, đồng nhất kích thước (Size 11-16 tùy vị trí).
    - **Tiêu đề:** Dịch toàn bộ tiêu đề trên cùng, căn giữa.
    - **Bố cục:** Sử dụng Table không viền. Cột trái chèn hình bàn cờ. Cột phải ghi các nước đi và lời bình.
    - **In đậm:** Chỉ in đậm tên các quân cờ: **Xe, Pháo, Mã, Tướng, Sĩ, Tượng, Chốt**.
    - **Ví dụ X:** Căn lề giữa.

## 2. Công cụ sử dụng
- **Ngôn ngữ:** Python
- **Thư viện:** `fitz` (PyMuPDF), `cv2` (OpenCV), `docx` (python-docx), `re` (Regex).
- **Môi trường:** `uv` (quản lý gói nhanh chóng).

## 3. Quy tắc vàng (Golden Rules)
- Không để dòng trống thừa trong bảng nước đi.
- Nước đi Đỏ và Đen cách nhau bởi dấu `...`.
- Tuyệt đối đồng nhất Font và Size trong cùng một dòng.
- Lưu file theo định dạng: `{số_trang}.docx`.
