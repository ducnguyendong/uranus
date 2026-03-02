# 🚀 Hệ Thống Phân Tích Thị Trường Crypto với OpenClaw

> **Kiến trúc tổng quan:** Gateway → Orchestrator Agent → Sub-agents (Price Monitor, On-chain Analyst, Sentiment Analyzer) → Tools (CoinGecko, Binance, Etherscan, TradingView) → Memory System

---

## 📁 Cấu Trúc Thư Mục Đề Xuất

```
openclaw-crypto/
├── MEMORY.md                        # Tổng quan hệ thống & trạng thái hiện tại
├── memory/
│   ├── portfolio.md                 # Danh mục đầu tư
│   ├── market_history.md            # Lịch sử biến động giá
│   ├── lessons_learned.md           # Bài học kinh nghiệm
│   ├── watchlist.md                 # Danh sách token theo dõi
│   └── sessions/
│       └── 2025-01-15_session.md    # Log từng phiên giao dịch
├── tools/
│   ├── coingecko_tool.py
│   ├── binance_tool.py
│   ├── etherscan_tool.py
│   ├── tradingview_tool.py
│   ├── telegram_notify.py
│   └── technical_analysis.py
├── agents/
│   ├── price_monitor.agent.md       # Sub-agent theo dõi giá
│   ├── onchain_analyst.agent.md     # Sub-agent on-chain
│   └── sentiment_agent.agent.md    # Sub-agent sentiment
├── heartbeat/
│   ├── hourly_summary.md            # Cron hàng giờ
│   ├── daily_report.md              # Cron hàng ngày
│   └── alert_rules.md               # Quy tắc cảnh báo
└── config/
    └── api_keys.env                 # API keys (không commit lên git)
```

---

## 1️⃣ PHÁT TRIỂN TOOLS (Công Cụ)

### Tool 1: CoinGecko — Lấy giá & market data

```python
# tools/coingecko_tool.py
"""
OpenClaw Tool: coingecko_market_data
Description: Lấy dữ liệu thị trường từ CoinGecko API (miễn phí, không cần API key cơ bản)
Usage: coingecko_market_data(coins="bitcoin,ethereum,solana", vs_currency="usd")
"""

import requests
import json
from datetime import datetime
from typing import Optional


def coingecko_market_data(
    coins: str = "bitcoin,ethereum",
    vs_currency: str = "usd",
    include_24h_change: bool = True
) -> dict:
    """
    Lấy dữ liệu market từ CoinGecko.
    
    Args:
        coins: Danh sách coin IDs, cách nhau bởi dấu phẩy
        vs_currency: Đơn vị tiền tệ (usd, vnd, eur...)
        include_24h_change: Có lấy % thay đổi 24h không
        
    Returns:
        dict: Dữ liệu đã được chuẩn hóa cho AI
    """
    base_url = "https://api.coingecko.com/api/v3"
    
    try:
        # Lấy giá + market data
        params = {
            "ids": coins,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": str(include_24h_change).lower(),
            "include_last_updated_at": "true"
        }
        response = requests.get(f"{base_url}/simple/price", params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
        
        # === XỬ LÝ JSON TỐI ƯU CHO AI ===
        # Chuẩn hóa thành ngôn ngữ tự nhiên + số liệu có nhãn
        summary = []
        structured = {}
        
        for coin_id, data in raw_data.items():
            price = data.get(vs_currency, 0)
            change_24h = data.get(f"{vs_currency}_24h_change", 0)
            market_cap = data.get(f"{vs_currency}_market_cap", 0)
            volume = data.get(f"{vs_currency}_24h_vol", 0)
            
            trend = "📈 tăng" if change_24h > 0 else "📉 giảm"
            
            # Plain text cho AI dễ reasoning
            summary.append(
                f"{coin_id.upper()}: ${price:,.2f} ({trend} {abs(change_24h):.2f}% 24h) "
                f"| MCap: ${market_cap/1e9:.2f}B | Vol: ${volume/1e6:.0f}M"
            )
            
            # Structured data cho queries cụ thể
            structured[coin_id] = {
                "price_usd": round(price, 4),
                "change_24h_pct": round(change_24h, 2),
                "market_cap_b": round(market_cap / 1e9, 2),
                "volume_24h_m": round(volume / 1e6, 2),
                "signal": "BULLISH" if change_24h > 5 else "BEARISH" if change_24h < -5 else "NEUTRAL"
            }
        
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": "\n".join(summary),        # AI đọc trực tiếp
            "data": structured,                    # Dùng cho logic
            "ai_context": f"Dữ liệu giá thời gian thực lúc {datetime.utcnow().strftime('%H:%M UTC')}. "
                         f"Các coin: {', '.join(structured.keys())}."
        }
        
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "CoinGecko API timeout. Thử lại sau 30 giây."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def coingecko_trending() -> dict:
    """Lấy top 7 coin trending trong 24h."""
    try:
        response = requests.get(
            "https://api.coingecko.com/api/v3/search/trending", 
            timeout=10
        )
        coins = response.json().get("coins", [])
        
        trending_list = []
        for item in coins[:7]:
            coin = item["item"]
            trending_list.append({
                "rank": coin["market_cap_rank"],
                "name": coin["name"],
                "symbol": coin["symbol"],
                "score": coin.get("score", 0)
            })
        
        return {
            "status": "success",
            "summary": "Top trending: " + ", ".join([f"{c['symbol']}(#{c['rank']})" for c in trending_list]),
            "trending": trending_list
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# === ENTRY POINT CHO OPENCLAW ===
if __name__ == "__main__":
    import sys
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    
    action = args.get("action", "market_data")
    
    if action == "trending":
        result = coingecko_trending()
    else:
        result = coingecko_market_data(
            coins=args.get("coins", "bitcoin,ethereum,solana"),
            vs_currency=args.get("vs_currency", "usd")
        )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

### Tool 2: Binance — Real-time klines & order book

```python
# tools/binance_tool.py
"""
OpenClaw Tool: binance_klines
Description: Lấy dữ liệu nến (OHLCV) và order book từ Binance (không cần API key cho public endpoints)
"""

import requests
import json
from datetime import datetime


def binance_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 24) -> dict:
    """
    Lấy dữ liệu nến từ Binance.
    
    interval: 1m, 5m, 15m, 1h, 4h, 1d, 1w
    limit: số nến tối đa (max 1000)
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw_klines = response.json()
        
        # Parse klines: [open_time, open, high, low, close, volume, ...]
        klines = []
        for k in raw_klines:
            klines.append({
                "time": datetime.utcfromtimestamp(k[0]/1000).strftime("%Y-%m-%d %H:%M"),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5])
            })
        
        # Tính toán nhanh cho AI
        if klines:
            last = klines[-1]
            first = klines[0]
            pct_change = ((last["close"] - first["open"]) / first["open"]) * 100
            max_high = max(k["high"] for k in klines)
            min_low = min(k["low"] for k in klines)
            avg_vol = sum(k["volume"] for k in klines) / len(klines)
            
            ai_summary = (
                f"{symbol} ({limit} nến {interval}): "
                f"Hiện tại ${last['close']:,.2f} | "
                f"Biến động: {pct_change:+.2f}% | "
                f"Range: ${min_low:,.2f} - ${max_high:,.2f} | "
                f"Vol TB: {avg_vol:,.0f}"
            )
            
            # Phát hiện pattern đơn giản
            patterns = []
            if last["close"] > last["open"]:
                body = last["close"] - last["open"]
                upper_wick = last["high"] - last["close"]
                if upper_wick < body * 0.1:
                    patterns.append("Marubozu tăng (bullish)")
            else:
                patterns.append("Nến giảm")
                
            # Kiểm tra volume spike
            if last["volume"] > avg_vol * 2:
                patterns.append("⚠️ Volume spike x2 (bất thường)")
        
        return {
            "status": "success",
            "symbol": symbol,
            "interval": interval,
            "summary": ai_summary,
            "patterns_detected": patterns,
            "latest_candle": last,
            "klines": klines[-10:],  # Trả về 10 nến gần nhất để tiết kiệm token
            "full_klines_count": len(klines)
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}


def binance_orderbook_pressure(symbol: str = "BTCUSDT", limit: int = 20) -> dict:
    """Phân tích áp lực mua/bán từ order book."""
    url = f"https://api.binance.com/api/v3/depth"
    
    try:
        response = requests.get(url, params={"symbol": symbol, "limit": limit}, timeout=10)
        data = response.json()
        
        bid_volume = sum(float(b[1]) for b in data["bids"])  # Lệnh mua
        ask_volume = sum(float(a[1]) for a in data["asks"])  # Lệnh bán
        
        ratio = bid_volume / (bid_volume + ask_volume)
        pressure = "MUA MẠNH 🟢" if ratio > 0.6 else "BÁN MẠNH 🔴" if ratio < 0.4 else "CÂN BẰNG ⚖️"
        
        return {
            "status": "success",
            "symbol": symbol,
            "bid_volume": round(bid_volume, 2),
            "ask_volume": round(ask_volume, 2),
            "buy_ratio": round(ratio * 100, 1),
            "pressure": pressure,
            "summary": f"{symbol} Order Book: {pressure} (Buy {ratio*100:.0f}% / Sell {(1-ratio)*100:.0f}%)"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import sys
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    action = args.get("action", "klines")
    
    if action == "orderbook":
        result = binance_orderbook_pressure(args.get("symbol", "BTCUSDT"))
    else:
        result = binance_klines(
            symbol=args.get("symbol", "BTCUSDT"),
            interval=args.get("interval", "1h"),
            limit=int(args.get("limit", 24))
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

### Tool 3: Etherscan — On-chain data

```python
# tools/etherscan_tool.py
"""
OpenClaw Tool: etherscan_onchain
Description: Theo dõi whale wallets, gas price, và giao dịch lớn trên Ethereum
Cần ETHERSCAN_API_KEY trong .env
"""

import requests
import json
import os
from datetime import datetime

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YourApiKey")
BASE_URL = "https://api.etherscan.io/api"


def get_gas_price() -> dict:
    """Lấy giá gas hiện tại của Ethereum."""
    params = {"module": "gastracker", "action": "gasoracle", "apikey": ETHERSCAN_API_KEY}
    
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        result = r.json().get("result", {})
        
        safe = int(result.get("SafeGasPrice", 0))
        fast = int(result.get("FastGasPrice", 0))
        
        return {
            "status": "success",
            "safe_gwei": safe,
            "fast_gwei": fast,
            "summary": f"⛽ ETH Gas: Safe={safe} Gwei | Fast={fast} Gwei",
            "recommendation": "Mạng tắc nghẽn, chờ giao dịch" if fast > 100 else "Mạng thông thoáng"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def watch_whale_wallet(address: str, min_value_eth: float = 100) -> dict:
    """Theo dõi các giao dịch lớn của một ví whale."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 20,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        transactions = r.json().get("result", [])
        
        large_txs = []
        for tx in transactions:
            value_eth = int(tx.get("value", 0)) / 1e18
            if value_eth >= min_value_eth:
                large_txs.append({
                    "hash": tx["hash"][:12] + "...",
                    "value_eth": round(value_eth, 2),
                    "time": datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime("%Y-%m-%d %H:%M"),
                    "direction": "OUT" if tx["from"].lower() == address.lower() else "IN"
                })
        
        return {
            "status": "success",
            "wallet": address[:8] + "...",
            "large_transactions": large_txs[:5],
            "summary": f"Ví {address[:8]}...: {len(large_txs)} giao dịch ≥{min_value_eth} ETH",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import sys
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    action = args.get("action", "gas")
    
    if action == "whale":
        result = watch_whale_wallet(args.get("address", ""), args.get("min_eth", 100))
    else:
        result = get_gas_price()
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## 2️⃣ SUB-AGENTS CHUYÊN BIỆT

### Sub-agent 1: Price Monitor (Theo dõi giá 24/7)

```markdown
<!-- agents/price_monitor.agent.md -->

# 🤖 Price Monitor Agent

## ROLE
Bạn là một chuyên gia giám sát giá crypto chạy liên tục. Nhiệm vụ là phát hiện 
biến động bất thường và gửi cảnh báo kịp thời.

## WATCHLIST
Đọc từ memory/watchlist.md để lấy danh sách coin cần theo dõi.

## QUY TRÌNH (mỗi lần kích hoạt)

1. Gọi tool `coingecko_market_data` với danh sách coin từ watchlist
2. Gọi tool `binance_klines` cho top 3 coin quan trọng nhất (interval=15m, limit=4)
3. So sánh với ngưỡng cảnh báo trong heartbeat/alert_rules.md
4. Nếu có cảnh báo → gọi tool `telegram_notify` với message được format sẵn
5. Ghi log vào memory/market_history.md

## NGƯỠNG CẢNH BÁO MẶC ĐỊNH
- Biến động > ±5% trong 1h → CẢNH BÁO CAO
- Biến động > ±10% trong 4h → CẢNH BÁO KHẨN CẤP
- Volume spike > 3x trung bình → THEO DÕI

## FORMAT BÁO CÁO VỀ AGENT CHÍNH
```json
{
  "agent": "price_monitor",
  "timestamp": "ISO8601",
  "alerts": [...],
  "summary": "text ngắn gọn",
  "action_required": true/false
}
```

## ESCALATION
Nếu action_required = true → Báo cáo ngay về Orchestrator Agent với tag [URGENT]
```

---

### Sub-agent 2: On-chain Analyst

```markdown
<!-- agents/onchain_analyst.agent.md -->

# 🔗 On-Chain Analyst Agent

## ROLE
Phân tích dữ liệu on-chain để phát hiện tín hiệu whale movement, 
gas anomaly, và smart money flow.

## QUY TRÌNH

1. Gọi `etherscan_onchain` để lấy gas price hiện tại
2. Kiểm tra các địa chỉ whale trong memory/watchlist.md (mục WHALE_WALLETS)
3. Phân tích patterns:
   - Whale accumulation (nhiều giao dịch IN liên tiếp)
   - Distribution (nhiều giao dịch OUT về exchange)
   - Gas spike (có thể báo hiệu NFT mint hoặc event lớn)
4. Tổng hợp thành "On-Chain Signal Score" từ -10 đến +10
5. Gửi Telegram nếu score > 7 hoặc < -7

## SIGNAL SCORE LOGIC
- Whale mua vào: +3 mỗi whale
- Whale bán ra về exchange: -3 mỗi whale  
- Gas tăng >200 Gwei: -1 (network congestion)
- Gas bình thường: 0

## OUTPUT FORMAT
```json
{
  "agent": "onchain_analyst",
  "onchain_signal_score": 6,
  "signal_label": "MODERATE_BULLISH",
  "key_events": ["Whale 0xABC... mua 500 ETH", "Gas bình thường 25 Gwei"],
  "recommendation": "Tích lũy cẩn thận, theo dõi thêm 2h"
}
```
```

---

### Tool: Telegram Notify

```python
# tools/telegram_notify.py
"""
OpenClaw Tool: telegram_notify
Description: Gửi thông báo/cảnh báo qua Telegram Bot
"""

import requests
import json
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(
    message: str,
    level: str = "INFO",  # INFO, WARNING, CRITICAL
    parse_mode: str = "HTML"
) -> dict:
    """
    Gửi alert qua Telegram.
    
    Telegram Bot setup:
    1. Chat với @BotFather → /newbot → lấy TOKEN
    2. Gửi tin nhắn cho bot → lấy CHAT_ID từ 
       https://api.telegram.org/bot{TOKEN}/getUpdates
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "error", "message": "Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env"}
    
    # Format message theo level
    level_emoji = {"INFO": "ℹ️", "WARNING": "⚠️", "CRITICAL": "🚨"}.get(level, "📢")
    
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
    
    lines = ["📊 <b>Market Report</b> — " + report_data.get("timestamp", "")[:16]]
    lines.append("─" * 30)
    
    for coin_id, d in coins.items():
        emoji = "🟢" if d["change_24h_pct"] > 0 else "🔴"
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
```

---

## 3️⃣ QUẢN LÝ KÝ ỨC (Memory System)

### MEMORY.md — Tệp tổng quan hệ thống

```markdown
<!-- MEMORY.md -->

# 🧠 Crypto Analysis Agent — System Memory

## TRẠNG THÁI HỆ THỐNG
- **Cập nhật lần cuối:** 2025-01-15 09:00 UTC
- **Chế độ hoạt động:** ACTIVE MONITORING
- **Thị trường hiện tại:** BULL RUN (BTC > $95,000)

## DANH MỤC ĐẦU TƯ (xem chi tiết: memory/portfolio.md)
| Coin | Số lượng | Giá mua TB | % Danh mục |
|------|----------|------------|------------|
| BTC  | 0.5      | $82,000    | 60%        |
| ETH  | 5.0      | $3,200     | 25%        |
| SOL  | 50       | $180       | 15%        |

## CHIẾN LƯỢC HIỆN TẠI
- Không mua thêm BTC khi RSI(1D) > 75
- DCA ETH mỗi khi giảm >8% trong 24h
- Stop-loss: -15% từ giá mua TB

## CÁC TÁC VỤ ĐANG THEO DÕI
- [ ] BTC phá kháng cự $100,000
- [ ] ETH/BTC ratio về 0.04 → tăng tỷ trọng ETH
- [x] SOL: Đã mua thêm 20 SOL ngày 2025-01-10

## LIÊN KẾT NỘI BỘ
- Chi tiết portfolio: [memory/portfolio.md]
- Lịch sử thị trường: [memory/market_history.md]  
- Bài học kinh nghiệm: [memory/lessons_learned.md]
```

### memory/lessons_learned.md — Kinh nghiệm giao dịch

```markdown
<!-- memory/lessons_learned.md -->

# 📚 Bài Học Kinh Nghiệm

## [2025-01-10] — Sự kiện FUD giả
- **Tình huống:** Tin đồn SEC kiện Binance → BTC -8% trong 2h
- **Hành động:** Hoảng loạn, bán ETH ở đáy
- **Kết quả:** ETH phục hồi +12% sau 6h
- **Bài học:** ⚠️ KHÔNG bán trong 2h đầu khi có FUD. Chờ xác nhận từ nguồn chính thức.
- **Quy tắc mới:** Khi FUD xuất hiện → chạy sentiment_agent trước khi quyết định

## [2025-01-05] — Volume spike SOL
- **Tình huống:** Volume SOL tăng 4x trong 1h
- **Hành động:** Mua thêm ngay lập tức
- **Kết quả:** +18% trong 24h
- **Bài học:** ✅ Volume spike + on-chain accumulation = tín hiệu tốt

## PATTERN ĐÃ KIỂM CHỨNG
1. BTC halving + 6 tháng → thường có bull run mạnh
2. Fear & Greed Index < 20 → vùng mua tốt cho BTC
3. ETH gas > 150 Gwei kéo dài → DeFi đang sôi động → tốt cho ETH
```

---

## 4️⃣ TỰ ĐỘNG HÓA VỚI CRON/HEARTBEAT

### Heartbeat: Tổng hợp thị trường hàng giờ

```markdown
<!-- heartbeat/hourly_summary.md -->

# ⏰ Hourly Market Summary — Cron Task

## LỊCH TRÌNH
- **Tần suất:** Mỗi 1 giờ (cron: 0 * * * *)
- **Trigger:** OpenClaw heartbeat scheduler

## QUY TRÌNH THỰC HIỆN

### Bước 1: Thu thập dữ liệu giá (Tools)
```
Gọi: coingecko_market_data(coins="bitcoin,ethereum,solana,bnb")
Gọi: binance_klines(symbol="BTCUSDT", interval="1h", limit=24)
Gọi: binance_orderbook_pressure(symbol="BTCUSDT")
```

### Bước 2: Kiểm tra on-chain
```
Gọi: etherscan_onchain(action="gas")
```

### Bước 3: Sentiment scan (dùng web_search có sẵn)
```
web_search("bitcoin crypto news last 1 hour")
web_search("crypto twitter trending now")
```

### Bước 4: Tổng hợp & đánh giá
- Tính Market Sentiment Score (0-100)
- So sánh với alert_rules.md
- Quyết định: HOLD / WATCH / ACT

### Bước 5: Output
- Nếu có cảnh báo → telegram_notify(level="WARNING/CRITICAL")
- Luôn ghi log vào memory/market_history.md
- Cập nhật MEMORY.md nếu có thay đổi chiến lược

## FORMAT LOG (ghi vào market_history.md)
```
## [2025-01-15 10:00 UTC]
- BTC: $96,500 (+1.2% 1h) | Sentiment: 68/100 GREED
- ETH: $3,450 (+0.8% 1h)
- Gas: 35 Gwei (bình thường)
- Signal: NEUTRAL — không có hành động
```
```

### Heartbeat: Báo cáo ngày + Sentiment từ X/Twitter

```markdown
<!-- heartbeat/daily_report.md -->

# 📅 Daily Market Report — Cron Task

## LỊCH TRÌNH  
- **Thời gian:** 8:00 SA (ICT) mỗi ngày
- **Cron:** 0 1 * * * (1:00 UTC = 8:00 ICT)

## QUY TRÌNH SENTIMENT ANALYSIS

### Bước 1: Thu thập tin tức
```
web_search("crypto market analysis today 2025")
web_search("bitcoin price prediction [ngày hôm nay]")
web_search("altcoin season 2025 latest")
web_search("crypto regulatory news today")
```

### Bước 2: Social Sentiment từ X/Twitter (qua web_search)
```
web_search("site:twitter.com bitcoin sentiment today")
web_search("crypto twitter fear greed today")
web_search("$BTC $ETH twitter trending analysis")
```

### Bước 3: Tổng hợp Fear & Greed
- Dùng browser tool → https://alternative.me/crypto/fear-and-greed-index/
- Đọc chỉ số F&G Index
- Phân tích: <25 = Extreme Fear (cơ hội mua), >75 = Extreme Greed (cẩn thận)

### Bước 4: Technical Overview
- Chụp ảnh TradingView (xem phần 5)
- Phân tích bằng Vision

### Output
1. Gửi báo cáo tổng hợp qua Telegram (telegram_notify)
2. Lưu vào memory/sessions/[date]_session.md
3. Cập nhật lessons_learned.md nếu có phát hiện mới
```

---

## 5️⃣ PHÂN TÍCH KỸ THUẬT VỚI BROWSER + VISION

### Tool: TradingView Screenshot + AI Vision

```python
# tools/tradingview_tool.py
"""
OpenClaw Tool: tradingview_capture
Description: Dùng browser tool để chụp ảnh biểu đồ TradingView rồi phân tích kỹ thuật bằng Vision
"""

import json

# URL công khai của TradingView (không cần đăng nhập)
TRADINGVIEW_CHART_URLS = {
    "BTCUSDT_1D": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=D",
    "BTCUSDT_4H": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=240",
    "ETHUSDT_1D": "https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT&interval=D",
    "BTCUSDT_WEEKLY": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=W",
    # Alternative: dùng TradingView widgets (embed, ít bị chặn hơn)
    "BTC_WIDGET": "https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=D&theme=dark"
}

# Prompt phân tích kỹ thuật cho AI Vision
TECHNICAL_ANALYSIS_PROMPT = """
Phân tích biểu đồ crypto này và cho biết:

1. **Xu hướng chính** (Uptrend/Downtrend/Sideways)
2. **Mô hình nến** trong 5 nến gần nhất (Doji, Hammer, Engulfing, Morning Star, v.v.)
3. **Các mức hỗ trợ/kháng cự** quan trọng (nêu mức giá cụ thể nếu thấy)
4. **Chỉ báo kỹ thuật** nếu hiển thị:
   - RSI: Oversold (<30) / Overbought (>70) / Neutral
   - MACD: Bullish crossover / Bearish crossover / Neutral
   - Bollinger Bands: Giá ở band trên/dưới/giữa
   - Volume: Tăng/giảm so với trung bình
5. **Tín hiệu trading:**
   - BUY signal: (điều kiện cụ thể)
   - SELL signal: (điều kiện cụ thể)
   - HOLD: (lý do)
6. **Mức giá quan trọng:** Entry point, Stop-loss, Take-profit (nếu xác định được)
7. **Độ tin cậy phân tích:** 1-10 (dựa trên rõ ràng của biểu đồ)

Trả lời ngắn gọn, súc tích, có thể dùng bullet points.
"""

def get_chart_analysis_prompt(symbol: str = "BTC", timeframe: str = "1D") -> dict:
    """
    Trả về URL và prompt để Agent dùng browser tool chụp và phân tích.
    Agent sẽ:
    1. Dùng browser tool mở URL
    2. Chụp screenshot
    3. Gửi ảnh + prompt vào Vision model
    """
    chart_key = f"{symbol}USDT_{timeframe}"
    url = TRADINGVIEW_CHART_URLS.get(chart_key, TRADINGVIEW_CHART_URLS["BTCUSDT_1D"])
    
    return {
        "status": "ready",
        "chart_url": url,
        "analysis_prompt": TECHNICAL_ANALYSIS_PROMPT,
        "instructions": (
            f"1. Mở URL: {url}\n"
            f"2. Chờ biểu đồ load (3-5 giây)\n"
            f"3. Chụp screenshot toàn màn hình\n"
            f"4. Phân tích ảnh với prompt đính kèm\n"
            f"5. Lưu kết quả vào memory/sessions/"
        ),
        "symbol": symbol,
        "timeframe": timeframe
    }


if __name__ == "__main__":
    import sys
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    result = get_chart_analysis_prompt(
        symbol=args.get("symbol", "BTC"),
        timeframe=args.get("timeframe", "1D")
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

---

## 6️⃣ CẤU HÌNH OPENCLAW CLI

### Đăng ký tất cả tools

```bash
# Đăng ký tools vào OpenClaw
openclaw tool add tools/coingecko_tool.py --name "coingecko_market_data" \
  --description "Lấy giá và market data từ CoinGecko"

openclaw tool add tools/binance_tool.py --name "binance_klines" \
  --description "Lấy dữ liệu nến OHLCV từ Binance"

openclaw tool add tools/etherscan_tool.py --name "etherscan_onchain" \
  --description "Dữ liệu on-chain: gas, whale wallets"

openclaw tool add tools/telegram_notify.py --name "telegram_notify" \
  --description "Gửi cảnh báo qua Telegram"

openclaw tool add tools/tradingview_tool.py --name "tradingview_capture" \
  --description "Chuẩn bị URL và prompt phân tích TradingView"

# Kiểm tra danh sách tools
openclaw tool list

# Test một tool cụ thể
openclaw tool test coingecko_market_data '{"coins": "bitcoin,ethereum", "vs_currency": "usd"}'
```

### Khởi chạy Sub-agents

```bash
# Khởi động price monitor sub-agent chạy nền
openclaw agent start agents/price_monitor.agent.md \
  --interval 15m \
  --name "price_monitor" \
  --background

# Khởi động on-chain analyst (chạy mỗi 30 phút)
openclaw agent start agents/onchain_analyst.agent.md \
  --interval 30m \
  --name "onchain_analyst" \
  --background

# Xem trạng thái các agents
openclaw agent status

# Xem log của agent cụ thể
openclaw agent logs price_monitor --tail 50
```

### Cấu hình Heartbeat/Cron

```bash
# Cron job: hourly summary
openclaw heartbeat create \
  --name "hourly_market" \
  --schedule "0 * * * *" \
  --task heartbeat/hourly_summary.md

# Cron job: daily report (8:00 ICT)
openclaw heartbeat create \
  --name "daily_report" \
  --schedule "0 1 * * *" \
  --task heartbeat/daily_report.md

# Xem lịch heartbeat
openclaw heartbeat list

# Chạy thủ công để test
openclaw heartbeat run hourly_market --now
```

### Chạy hệ thống hoàn chỉnh

```bash
# Set API keys
export ETHERSCAN_API_KEY="your_key_here"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# Khởi động toàn bộ hệ thống
openclaw start \
  --memory MEMORY.md \
  --agents agents/ \
  --heartbeat heartbeat/ \
  --tools tools/

# Chat trực tiếp với agent
openclaw chat
> "Phân tích thị trường BTC hiện tại và cho tôi lời khuyên có nên mua không"
> "Chụp biểu đồ ETH/USDT khung 4h và phân tích kỹ thuật"
> "Tổng hợp sentiment từ Twitter về crypto hôm nay"
```

---

## 7️⃣ FLOW TÍCH HỢP HOÀN CHỈNH

```
[Heartbeat 15 phút]
        │
        ▼
[coingecko_market_data] ──→ Giá mới nhất
[binance_klines]         ──→ Nến + Volume
[etherscan_onchain]      ──→ Gas + Whale
        │
        ▼
[Orchestrator Agent phân tích]
        │
        ├── Bình thường ──→ Ghi log memory/market_history.md
        │
        └── Bất thường ──→ [telegram_notify: CRITICAL]
                          [Gọi tradingview_capture]
                          [Chụp chart + Vision Analysis]
                          [Ghi lessons_learned.md nếu có bài học]
                          [Cập nhật MEMORY.md]
```

---

## 📌 CHECKLIST TRIỂN KHAI

- [ ] Clone repo OpenClaw và cài đặt dependencies
- [ ] Tạo Telegram Bot qua @BotFather, lấy TOKEN + CHAT_ID
- [ ] Đăng ký API key Etherscan (miễn phí tại etherscan.io)
- [ ] Copy tất cả tools vào thư mục `tools/`
- [ ] Tạo các file memory theo cấu trúc trên
- [ ] Đăng ký tools: `openclaw tool add ...`
- [ ] Khởi động sub-agents background
- [ ] Cấu hình heartbeat/cron
- [ ] Test bằng `openclaw chat`
- [ ] Kiểm tra Telegram nhận được tin nhắn test

---

*Tài liệu này được tạo cho hệ thống OpenClaw Crypto Analysis — Cập nhật: 2025-01-15*
