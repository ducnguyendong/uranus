import requests
import json
import os

# Cấu hình Token của Crypto Bot và Chat ID từ file api_keys.env
TELEGRAM_BOT_TOKEN = "8729529558:AAF5ptYRPCeFnjmZEs3UJZGawhwUsx4ie9M" 
TELEGRAM_CHAT_ID = "1881519352" 

def send_telegram_alert(message: str) -> dict:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"❄️ <b>OpenClaw Crypto Report</b>\n\n{message}",
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else "Demo report from Uranus Crypto Bot"
    print(json.dumps(send_telegram_alert(msg), ensure_ascii=False, indent=2))
