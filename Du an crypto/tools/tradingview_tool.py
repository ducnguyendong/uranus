import json

TRADINGVIEW_CHART_URLS = {
    "BTCUSDT_1D": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=D",
    "BTCUSDT_4H": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=240",
    "ETHUSDT_1D": "https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT&interval=D",
    "BTCUSDT_WEEKLY": "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT&interval=W",
    "BTC_WIDGET": "https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=D&theme=dark"
}

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
