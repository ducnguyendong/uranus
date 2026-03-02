import requests
import json
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(
    message: str,
    level: str = "INFO",
    parse_mode: str = "HTML"
) -> dict:
    """
    Gửi alert qua Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "error", "message": "Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env"}
    
    level_emoji = {"INFO": "ℹ️", "WARNING": "⚠️", "CRITICAL": "🚨"}.get(level, "🔔")
    
    formatted_message = f"{level_emoji} <b>[{level}] OpenClaw Crypto Alert</b>\n\n{message}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": formatted_message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return {"status": "success", "message_id": response.json()["result"]["message_id"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_market_report(report_data: dict) -> dict:
    """Format và gửi báo cáo thị trường đẹp qua Telegram."""
    coins = report_data.get("data", {})
    
    lines = ["📊 <b>Market Report</b> – " + report_data.get("timestamp", "")[:16]]
    lines.append("-" * 30)
    
    for coin_id, d in coins.items():
        emoji = "📈" if d["change_24h_pct"] > 0 else "📉"
        lines.append(
            f"{emoji} <b>{coin_id.upper()}</b>: ${d['price_usd']:,} "
            f"({d['change_24h_pct']:+.1f}%)"
        )
    
    message = "\n".join(lines)
    return send_telegram_alert(message, level="INFO")

if __name__ == "__main__":
    import sys
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    
    action = args.get("action", "send")
    if action == "report":
        result = send_market_report(args.get("report_data", {}))
    else:
        result = send_telegram_alert(
            message=args.get("message", "Test từ OpenClaw"),
            level=args.get("level", "INFO")
        )
    print(json.dumps(result, ensure_ascii=False))
