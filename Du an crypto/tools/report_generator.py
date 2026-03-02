import sys
import os
import json
import subprocess
from datetime import datetime
import requests

# Import local tools from workspace
WORKSPACE_PATH = r"C:\Users\Nguyendd\.openclaw\workspace\Du an crypto\tools"
sys.path.append(WORKSPACE_PATH)

import coingecko_tool
import etherscan_tool
import telegram_tool

def get_crypto_news():
    """Lấy tin tức crypto trong 1 giờ qua (giả lập hoặc dùng API đơn giản)"""
    # Vì đây là script chạy độc lập, ta sẽ dùng một nguồn tin RSS hoặc API tin tức đơn giản
    # Trong môi trường OpenClaw, agent sẽ dùng web_search, nhưng script này cần tự chạy.
    # Tạm thời lấy tin từ một nguồn công khai hoặc để trống để Agent điền vào.
    return [
        "Thị trường đang nén chặt chờ đợi tin tức vĩ mô.",
        "Dòng tiền từ các quỹ ETF vẫn đang duy trì ổn định."
    ]

def generate_hourly_report():
    # 1. Lấy giá
    price_data = coingecko_tool.coingecko_market_data()
    prices = price_data.get("data", {})
    
    # 2. Check Gas
    gas_data = etherscan_tool.get_gas_price()
    
    # 3. Format báo cáo theo mẫu anh Nguyên thích
    now_str = datetime.now().strftime("%I:%M %p")
    
    report = f"🕒 Crypto Hourly Report ({now_str})\n\n"
    
    # Mục 1: Biến động giá
    report += "1. Biến động giá (Coingecko):\n"
    emoji_map = {"bitcoin": "🟠", "ethereum": "🔵", "solana": "🟣", "pi-network": "⚡"}
    for coin, info in prices.items():
        emoji = emoji_map.get(coin, "💰")
        name = coin.replace("-network", "").upper()
        change = info['change_24h_pct']
        trend = "+" if change > 0 else ""
        report += f"• {emoji} {name}: {info['price_usd']:,.2f} USD ({trend}{change}% 24h)\n"
    
    # Mục 2: On-chain & Hệ thống
    report += "\n2. On-chain & Hệ thống:\n"
    if gas_data.get("status") == "success":
        safe = gas_data['safe_gwei']
        report += f"• ⛽ ETH Gas: {safe:.4f} Gwei "
        if safe < 1:
            report += "(Rẻ như cho, anh tranh thủ làm task đi ạ!)\n"
        elif safe < 20:
            report += "(Mức phí thấp, giao dịch mượt mà)\n"
        else:
            report += "(Phí hơi cao, anh nên cân nhắc)\n"
    report += "• 🛠 Trạng thái: Hệ thống Uranus đang trực chiến 24/7.\n"
    
    # Mục 3: Tin tức (Sẽ được Agent bổ sung hoặc lấy mặc định)
    report += "\n3. Tin tức nóng hổi (1h qua):\n"
    news = get_crypto_news()
    for item in news:
        report += f"• {item}\n"
    
    # Mục 4: Nhận định nhanh
    report += "\n4. Nhận định nhanh:\n"
    btc_change = prices.get("bitcoin", {}).get("change_24h_pct", 0)
    if btc_change < -2:
        report += "Thị trường đang có nhịp điều chỉnh, anh nên quan sát các mốc hỗ trợ cứng."
    elif btc_change > 2:
        report += "Đà tăng đang khá tốt, dòng tiền đang đổ mạnh vào hệ sinh thái."
    else:
        report += "Giá đang đi ngang tích lũy, mức Gas thấp là cơ hội tốt để cơ cấu lại danh mục."

    # Gửi qua Telegram
    telegram_tool.send_telegram_alert(report)
    return report

if __name__ == "__main__":
    print(generate_hourly_report())
