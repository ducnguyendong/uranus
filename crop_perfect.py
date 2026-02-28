
import fitz  # PyMuPDF
import PIL.Image as Image
import io

def manual_precision_crop(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Render trang ở DPI cao (400) để đảm bảo độ sắc nét
    zoom = 400 / 72
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix)
    
    # Chuyển sang ảnh PIL
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    w, h = img.size
    
    # Tọa độ tương đối (đã soi kỹ từ trang 14)
    # Bàn cờ trong trang này nằm ở khoảng giữa.
    # Ta sẽ cắt một vùng tập trung vào trung tâm và điều chỉnh tỷ lệ.
    
    # Cắt chính xác vùng bàn cờ dựa trên phân tích hình ảnh minh họa
    # [trái, trên, phải, dưới] tính theo tỷ lệ % của trang để đảm bảo ổn định
    # Dựa trên hình ảnh 14.pdf:
    left = 0.12 * w
    top = 0.42 * h
    right = 0.88 * w
    bottom = 0.77 * h
    
    board = img.crop((left, top, right, bottom))
    board.save(output_path, "PNG")
    return True

pdf_file = r"D:\Du an dich tan cuc dai toan\14.pdf"
final_output = r"D:\Du an dich tan cuc dai toan\output\14\board_perfect.png"

manual_precision_crop(pdf_file, final_output)
print("DONE_PERFECT")
