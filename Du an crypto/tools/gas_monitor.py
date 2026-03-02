import sys
import os
import time
from datetime import datetime

# Đảm bảo in được tiếng Việt trên console Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thêm root vào sys.path để import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from etherscan_tool import get_gas_price

def check_gas_alert(threshold=50.0):
    """Kiểm tra giá Gas và in cảnh báo nếu vượt ngưỡng."""
    result = get_gas_price()
    
    if result["status"] == "success":
        gas = result["propose_gwei"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{timestamp}] Kiểm tra Gas ETH: {gas:.4f} Gwei")
        
        if gas >= threshold:
            print("\n" + "!" * 50)
            print(f"🚨 CẢNH BÁO ĐỎ: GAS ETHEREUM VƯỢT NGƯỠNG ({threshold} Gwei)!")
            print(f"Giá hiện tại: {gas:.4f} Gwei")
            print("Khuyến nghị: Tạm hoãn các giao dịch không cấp thiết.")
            print("!" * 50 + "\n")
            return True
        elif gas >= threshold * 0.7:
             print(f"⚠️ Chú ý: Gas đang tăng ({gas:.4f} Gwei), gần ngưỡng cảnh báo.")
             return False
        else:
            print(f"✅ Gas đang ở mức an toàn ({gas:.4f} Gwei). Thoải mái 'đi chợ' anh nhé!")
            return False
    else:
        print(f"❌ Lỗi khi kiểm tra Gas: {result.get('message')}")
        return False

if __name__ == "__main__":
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
    check_gas_alert(threshold)
