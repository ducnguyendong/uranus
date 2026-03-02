# 🕒 Hourly Market Summary

## QUY TRÌNH THỰC HIỆN
1. **Lấy giá**: Chạy `python "Du an crypto/tools/coingecko_tool.py"` để xem giá BTC, ETH, SOL.
2. **Check Gas**: Chạy `python "Du an crypto/tools/etherscan_tool.py"` (đã giới hạn tốc độ call).
3. **Tin tức**: Dùng web_search tìm kiếm \crypto news last 1 hour\.
4. **Cảnh báo Gas**: Chạy `python "Du an crypto/tools/gas_monitor.py" 50` để kiểm tra ngưỡng an toàn.
5. **Báo cáo**: Nếu giá biến động > 2% hoặc Gas > 80 Gwei, gửi tin nhắn qua Telegram.

## MẪU BÁO CÁO CHUẨN (Gửi qua Telegram)
1. **Biến động giá (CoinGecko)**: BTC, ETH, SOL (+% 24h) kèm ghi chú ngắn.
2. **Tình hình On-chain & Hệ thống**: Gas ETH (độ chính xác thập phân), trạng thái các tool.
3. **Tin tức nóng hổi**: Tổng hợp tin trong 1h qua (dùng web_search).
4. **Nhận định nhanh**: Đánh giá tổng quan thị trường và lực mua/bán.
