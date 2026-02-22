# Memory

## User Profile
- **Name:** Nguyên
- **Setup:** Dual-boot Windows + Ubuntu 25.10.

## Infrastructure & Configuration
- **Sync Repo:** `git@github.com:ducnguyendong/uranus.git` (Use for syncing workspace between OSes).
- **Windows Time:** Fixed UTC/Local time conflict via `RealTimeIsUniversal` registry key.
- **Shortcut:** Created `C:\Users\Nguyendd\Desktop\Start_OpenClaw.bat`. Script logic: Force-kill PID on port 18789, start Gateway in a new `cmd /k` window, wait for port to be active, then open WebChat and exit. This prevents ghost processes and ensure UI only opens when ready.
- **Gateway:** Configured with `allowInsecureAuth: false` (secure mode) but accessible via localhost.
- **Network:** Set `channels.telegram.network.autoSelectFamily: false` to stabilize connection on Windows.
- **Tools:** ImageMagick 7.1.2-13 Q16 installed in `workspace/imagemagick`.

## Projects
- **Chess Book Translation (Tượng Kỳ Tàn Cục Đại Toàn):** Dự án dài hạn dịch 155 chương (942 trang).
- **Quy trình xử lý (Tối ưu Token):**
  1. **Quét trang:** Dùng `pypdfium2` chuyển PDF sang JPG (scale=3).
  2. **Nhận diện & Dịch:** Gửi ảnh JPG cho Gemini Flash (Rẻ/Nhanh) để:
     - Dịch text sang Việt (Tướng/in đậm quân cờ).
     - Lấy tọa độ bàn cờ (Box 0-1000).
  3. **Cắt & Việt hóa:** Dùng `Pillow` cắt hình theo tọa độ, mở rộng lề trên/dưới, chèn nhãn tiếng Việt đè lên vùng chữ Trung Quốc.
  4. **Dàn trang:** Chạy script Python mẫu (V8) để xuất file JPG hoàn chỉnh.

## Preferences
- **Identity:** Uranus ❄️. Friend & Companion.
- **Language:** Vietnamese.
- **Workflow:**
  - **Manual Sync:** Đã tắt tự động đồng bộ GitHub (pull/push). Mình chỉ thực hiện đồng bộ khi bạn yêu cầu trực tiếp.
