import requests
import json
import os
import time
from datetime import datetime, timezone

# Lấy API key
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YSU35FFKYYQSFYUPBVKRSVGEPGPAPRC4FH")
# Etherscan API V2 Base URL
BASE_URL = "https://api.etherscan.io/v2/api"

def get_gas_price(chainid: int = 1) -> dict:
    """Lấy giá gas hiện tại của Ethereum qua API V2."""
    params = {
        "chainid": chainid,
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": ETHERSCAN_API_KEY
    }
    
    try:
        time.sleep(0.25)
        r = requests.get(BASE_URL, params=params, timeout=10)
        res_json = r.json()
        
        if res_json.get("status") == "0":
            return {"status": "error", "message": res_json.get("result")}
            
        result = res_json.get("result", {})
        safe = int(result.get("SafeGasPrice", 0))
        fast = int(result.get("FastGasPrice", 0))
        
        return {
            "status": "success",
            "safe_gwei": safe,
            "fast_gwei": fast,
            "summary": f"ETH Gas: Safe={safe} Gwei | Fast={fast} Gwei"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def watch_whale_wallet(address: str, chainid: int = 1, min_value_eth: float = 100) -> dict:
    """Theo dõi các giao dịch lớn của một ví whale qua API V2."""
    params = {
        "chainid": chainid,
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 10,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    
    try:
        time.sleep(0.25)
        r = requests.get(BASE_URL, params=params, timeout=10)
        res_json = r.json()
        
        if res_json.get("status") == "0" and res_json.get("message") != "No transactions found":
            return {"status": "error", "message": res_json.get("result")}
            
        transactions = res_json.get("result", [])
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
                        "time": datetime.fromtimestamp(int(tx["timeStamp"]), timezone.utc).strftime("%Y-%m-%d %H:%M"),
                        "direction": "OUT" if tx["from"].lower() == address.lower() else "IN"
                    })
        
        return {
            "status": "success",
            "wallet": address[:8] + "...",
            "large_transactions": large_txs,
            "summary": f"Ví {address[:8]}...: {len(large_txs)} giao dịch lớn được tìm thấy."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    try:
        args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    except:
        args = {}
        
    action = args.get("action", "gas")
    if action == "whale":
        result = watch_whale_wallet(args.get("address", "0xAb5801a7D12701505BC94C2222302456e5fCC3f6"))
    else:
        result = get_gas_price()
        
    print(json.dumps(result, ensure_ascii=False, indent=2))
