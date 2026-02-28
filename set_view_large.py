import os

root_dir = r"D:\Du an dich tan cuc dai toan"

def set_folder_to_pictures(folder_path):
    ini_path = os.path.join(folder_path, "desktop.ini")
    ini_content = "[.ShellClassInfo]\r\n[ViewState]\r\nMode=\r\nVid=\r\nFolderType=Pictures\r\n"
    
    try:
        # Tạo file desktop.ini
        with open(ini_path, "w", encoding="utf-16") as f:
            f.write(ini_content)
        
        # Thiết lập thuộc tính ẩn và hệ thống cho file desktop.ini
        os.system(f'attrib +h +s "{ini_path}"')
        
        # Thiết lập thuộc tính Read-only cho thư mục (để Windows kích hoạt desktop.ini)
        os.system(f'attrib +r "{folder_path}"')
    except Exception as e:
        print(f"Error at {folder_path}: {e}")

def run_all():
    # Quét tất cả thư mục con từ 1 đến 942
    folders = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    for folder in folders:
        full_path = os.path.join(root_dir, folder)
        set_folder_to_pictures(full_path)
    print("Success: Set Pictures mode for all folders!")

if __name__ == "__main__":
    run_all()
