import requests
import json
from datetime import datetime, timezone

def coingecko_market_data(
    coins: str = "bitcoin,ethereum,solana",
    vs_currency: str = "usd",
    include_24h_change: bool = True
) -> dict:
    base_url = "https://api.coingecko.com/api/v3"
    try:
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
        
        summary = []
        structured = {}
        
        for coin_id, data in raw_data.items():
            price = data.get(vs_currency, 0)
            change_24h = data.get(f"{vs_currency}_24h_change", 0)
            market_cap = data.get(f"{vs_currency}_market_cap", 0)
            volume = data.get(f"{vs_currency}_24h_vol", 0)
            
            trend = "[UP]" if change_24h > 0 else "[DOWN]"
            
            summary.append(
                f"{coin_id.upper()}: ${price:,.2f} ({trend} {abs(change_24h):.2f}% 24h) "
                f"| MCap: ${market_cap/1e9:.2f}B | Vol: ${volume/1e6:.0f}M"
            )
            
            structured[coin_id] = {
                "price_usd": round(price, 4),
                "change_24h_pct": round(change_24h, 2),
                "market_cap_b": round(market_cap / 1e9, 2),
                "volume_24h_m": round(volume / 1e6, 2)
            }
        
        return {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": "\n".join(summary),
            "data": structured
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = coingecko_market_data()
    # In ra với mã hóa UTF-8 để tránh lỗi Windows console
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output.encode('utf-8').decode('utf-8'))
