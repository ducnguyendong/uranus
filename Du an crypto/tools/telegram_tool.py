import requests
import json
import os
import sys

# Đảm bảo in được tiếng Việt trên console Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình Token của Crypto Bot và Chat ID từ file api_keys.env
TELEGRAM_BOT_TOKEN = "8729529558:AAF5ptYRPCeFnjmZEs3UJZGawhwUsx4ie9M" 
TELEGRAM_CHAT_ID = "1881519352" 

def send_telegram_alert(message: str) -> dict:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Debug: In ra tin nhắn sẽ gửi để kiểm tra
    # print(f"DEBUG SEND: {message}")
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"❄️ OpenClaw Crypto Report\n\n{message}"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    # Ghép tất cả các tham số lại thành một chuỗi duy nhất nếu có nhiều tham số
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Demo report from Uranus Crypto Bot"
    print(json.dumps(send_telegram_alert(msg), ensure_ascii=False, indent=2))
