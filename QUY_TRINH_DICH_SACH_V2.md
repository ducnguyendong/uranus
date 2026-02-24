# QUY TRÌNH DỊCH SÁCH CỜ TƯỚNG CHUẨN (V2.0)

Quy trình này được tối ưu để tránh nhầm lẫn hình ảnh và đảm bảo tính đồng nhất tuyệt đối cho toàn bộ 942 trang sách.

## 1. Các bước thực hiện

### Bước 1: Trích xuất Dữ liệu (Marker AI)
- Chạy `marker_single` để lấy file Markdown và các file ảnh đã tách rời.
- Lưu kết quả vào thư mục `marker_output/{trang}`.

### Bước 2: Phân tích & Khớp nối (Vision Mapping)
- Gửi ảnh gốc của trang (300 DPI) cho Gemini.
- Yêu cầu Gemini:
    - Trích xuất text tiếng Việt theo văn phong chuyên môn.
    - Xác định số lượng Ví dụ và Hình ảnh.
    - **Quan trọng:** Chỉ rõ ảnh nào (Figure mấy của Marker) tương ứng với Ví dụ nào dựa trên nội dung thế cờ.

### Bước 3: Kiểm soát Bố cục & Định dạng
- **Tên file:** `{trang}.docx` (Không thêm hậu tố).
- **Font:** Times New Roman toàn bộ.
- **Size:** Tiêu đề (16), Tiết (14), Nội dung/Nước đi (11).
- **Bôi đậm:** Chỉ bôi đậm tên quân cờ: **Xe, Pháo, Mã, Tướng, Sĩ, Tượng, Chốt**.
- **Nước đi:** Gộp Đỏ ... Đen trên một dòng (Ví dụ: `1. Chốt 4 bình 5 ... Tướng 5 thoái 1`).
- **Hình ảnh:** Căn giữa trong cột trái của bảng. Chú thích hình (Hình X) nằm ngay dưới ảnh, in nghiêng.

### Bước 4: Đóng gói (Python Docx)
- Sử dụng script tự động để lắp ráp text và ảnh vào template Word chuẩn.

## 2. Quy tắc chống sai sót
- Luôn đối chiếu thế cờ trong ảnh với các nước đi trong văn bản trước khi xuất file.
- Tuyệt đối không để dòng trống trong phần liệt kê nước đi.
- Căn giữa dòng "Ví dụ X".
