import requests
import json
import os
import time
from datetime import datetime

# Lấy API key từ môi trường
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YSU35FFKYYQSFYUPBVKRSVGEPGPAPRC4FH")
BASE_URL = "https://api.etherscan.io/api"

def get_gas_price() -> dict:
    """Lấy giá gas hiện tại của Ethereum."""
    params = {"module": "gastracker", "action": "gasoracle", "apikey": ETHERSCAN_API_KEY}
    
    try:
        # Giới hạn tốc độ: Nghỉ 0.25s để đảm bảo không vượt quá 5 calls/s
        time.sleep(0.25)
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
        # Giới hạn tốc độ cho Whale Check
        time.sleep(0.25)
        r = requests.get(BASE_URL, params=params, timeout=10)
        transactions = r.json().get("result", [])
        
        large_txs = []
        if isinstance(transactions, list):
            for tx in transactions:
                try:
                    value_eth = int(tx.get("value", 0)) / 1e18
                except:
                    continue
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
            "summary": f"Ví {address[:8]}...: {len(large_txs)} giao dịch ≥ {min_value_eth} ETH",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    # Nhận tham số từ OpenClaw exec
    try:
        args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    except:
        args = {}
        
    action = args.get("action", "gas")
    
    if action == "whale":
        result = watch_whale_wallet(args.get("address", ""), args.get("min_eth", 100))
    else:
        result = get_gas_price()
        
    print(json.dumps(result, ensure_ascii=False, indent=2))
