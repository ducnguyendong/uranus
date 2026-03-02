import requests
import json
from datetime import datetime

def binance_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 24) -> dict:
    """
    Lấy dữ liệu nến từ Binance.
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw_klines = response.json()
        
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
            
            patterns = []
            if last["close"] > last["open"]:
                body = last["close"] - last["open"]
                upper_wick = last["high"] - last["close"]
                if upper_wick < body * 0.1:
                    patterns.append("Marubozu tăng (bullish)")
            else:
                patterns.append("Nến giảm")
                
            if last["volume"] > avg_vol * 2:
                patterns.append("🚀 Volume spike x2 (bất thường)")
        
        return {
            "status": "success",
            "symbol": symbol,
            "interval": interval,
            "summary": ai_summary,
            "patterns_detected": patterns,
            "latest_candle": last,
            "klines": klines[-10:],
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
        
        bid_volume = sum(float(b[1]) for b in data["bids"])
        ask_volume = sum(float(a[1]) for a in data["asks"])
        
        ratio = bid_volume / (bid_volume + ask_volume)
        pressure = "MUA MẠNH 🔥" if ratio > 0.6 else "BÁN MẠNH ❄️" if ratio < 0.4 else "CÂN BẰNG ⚖️"
        
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
