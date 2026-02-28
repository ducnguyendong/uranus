# DỰ ÁN: SỐ HÓA CỔ PHỔ CỜ TƯỚNG
## Uranus Visionary Scribe (Engine v5.0 - Full Batch Mode)

### 🛠️ Công cụ & Hệ thống:
- **Lõi xử lý:** Marker (AI OCR), PyMuPDF, OpenCV, Python-Docx, Regex.
- **AI Models:** Gemini Flash Vision (dịch thuật), Google Embeddings.
- **Tiện ích:** Pandoc v3.1.11 (Markdown -> Docx), Brave Search API (Hạn mức 1000 req/tháng).
- **Kênh thông báo:** Telegram Uranus Mirror Bridge (ID: 1881519352).

### ⚙️ Quy trình 3 Giai đoạn (Engine v5.0)
1. **Giai đoạn 1: Khai thác (Local - 0 Token):**
   - **Cắt ảnh:** Dùng Contours v6 trích xuất toàn bộ bàn cờ.
   - **OCR Thô:** Dùng Marker chuyển PDF sang Markdown để lấy cấu trúc chữ và vị trí ảnh.
2. **Giai đoạn 2: Tinh luyện (AI Vision - Tiết kiệm Token):**
   - Đối chiếu MD thô + Ảnh để Gemini Flash Vision dịch sang văn phong cờ tướng Việt Nam.
3. **Giai đoạn 3: Đóng gói (Automated):**
   - Tự động đúc file Word (.docx) chuẩn chuyên gia qua `uranus_master_docx.py`.

### ✅ Tiến độ (Cập nhật 17:00 26/02/2026)
- **Hoàn thiện (Giai đoạn 2 & 3):** Đã xong đến trang **28**. Bản Word v2 (Căn giữa ảnh + Chú thích in nghiêng) đã lưu tại ổ D.
- **Giai đoạn 1 (OCR Thô):** Đã xong đến trang **120**.
- **Tối ưu hóa ảnh:** Toàn bộ **942 trang** đã được nén xuống chiều cao chuẩn 2000px để tiết kiệm TPM.
- **Quy hoạch PDF:** Toàn bộ 942 file PDF đã được di chuyển vào đúng thư mục trang tương ứng.

### 🚀 Quy trình "Lai" (Hybrid) - Uranus Master v1.0
1. **Sub-agent (Vision):** Dịch và trả về nội dung Markdown kèm thẻ `[[HÌNH_X]] (Hình Y)`. (Sử dụng model Gemini-Flash-Latest, fresh session để tránh tích tụ context).
2. **Master Script (`uranus_master_docx.py`):** Uranus trực tiếp chạy lệnh đóng gói, tự động nhận diện file `board_X.png` trong thư mục để chèn vào Word.
3. **Nghỉ giữa hiệp:** Nghỉ 2 phút sau mỗi 4 trang để "xả" TPM.

### 🛠️ Công cụ sẵn sàng:
- `uranus_master_docx.py`: Script đóng gói Word chuyên nghiệp.
- Embeddings: Đã chuyển sang **Google (Gemini)** mượt mà, không tốn quota OpenAI.

### 📲 Uranus Mirror Bridge
- **Telegram ID:** `1881519352` (anh Nguyên).
- **Trạng thái:** Đã thông suốt (vừa test thành công).
