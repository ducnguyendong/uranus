import os
import subprocess
import shutil
import argparse
from pathlib import Path

# QUY TRÌNH OCR THÔ SIÊU SẠCH (Uranus Marker Engine v2.1 - Batch Mode)

def run_clean_ocr(input_pdf, output_folder):
    print(f"--- ĐANG CHẠY OCR THÔ SIÊU SẠCH CHO: {input_pdf} ---")
    try:
        # Sử dụng đường dẫn tuyệt đối đến marker_single.exe và bỏ --langs
        marker_path = r"C:\Users\Nguyendd\AppData\Roaming\Python\Python312\Scripts\marker_single.exe"
        # Chạy để lấy markdown và json
        command = f"\"{marker_path}\" \"{input_pdf}\" --output_dir \"{output_folder}\""
        subprocess.run(command, shell=True, check=True)
        
        # Sau khi chạy marker_single, Marker thường tạo thư mục con trùng tên file
        # Chúng ta cần tìm file content.json trong đó và đưa ra ngoài output_folder
        pdf_stem = Path(input_pdf).stem
        marker_out_dir = Path(output_folder) / pdf_stem
        
        if marker_out_dir.exists():
            for item in marker_out_dir.glob("*"):
                if item.suffix.lower() in ['.json', '.md']:
                    shutil.copy(item, Path(output_folder) / item.name)
            
            # Xóa sạch các file ảnh rác và thư mục figures
            for item in marker_out_dir.rglob("*"):
                if item.is_file() and item.suffix.lower() in ['.jpeg', '.jpg', '.png'] and "_Figure_" in item.name:
                    os.remove(item)
            
            figures_dir = marker_out_dir / "figures"
            if figures_dir.exists():
                shutil.rmtree(figures_dir)
        
        print(f"Hoàn thành trang {pdf_stem}!")
        
    except Exception as e:
        print(f"Lỗi xử lý {input_pdf}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--end', type=int, required=True)
    args = parser.parse_args()

    base_path = Path(r"D:\Du an dich tan cuc dai toan - moi")
    
    for page in range(args.start, args.end + 1):
        page_dir = base_path / str(page)
        pdf_file = page_dir / f"{page}.pdf"
        
        if not pdf_file.exists():
            print(f"Không tìm thấy: {pdf_file}")
            continue
            
        run_clean_ocr(str(pdf_file), str(page_dir))

if __name__ == "__main__":
    main()
