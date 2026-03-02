import requests
import json
import os
import time
from datetime import datetime, timezone

# Etherscan API Key của anh Nguyên
ETHERSCAN_API_KEY = "YSU35FFKYYQSFYUPBVKRSVGEPGPAPRC4FH"
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
        # V2 trả về giá trị có phần thập phân nên giữ nguyên float
        safe = float(result.get("SafeGasPrice", 0))
        propose = float(result.get("ProposeGasPrice", 0))
        fast = float(result.get("FastGasPrice", 0))
        
        return {
            "status": "success",
            "safe_gwei": safe,
            "propose_gwei": propose,
            "fast_gwei": fast,
            "summary": f"ETH Gas: Safe={safe:.4f} Gwei | Fast={fast:.4f} Gwei"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = get_gas_price()
    print(json.dumps(result, ensure_ascii=False, indent=2))
