from openpyxl.styles import Font  # Thêm import này

# Hàm để tạo file Excel trong bộ nhớ
def create_excel(links):
    wb = Workbook()
    ws = wb.active
    ws.title = "Links"
    
    # Ghi các nhãn cho hàng số 1 và thiết lập font cho các ô
    ws['A1'] = 'Liên kết gốc'
    ws['B1'] = 'Sub_id1'
    ws['C1'] = 'Sub_id2'
    ws['D1'] = 'Sub_id3'
    ws['E1'] = 'Sub_id4'
    ws['F1'] = 'Sub_id5'

    # Thiết lập font chữ Arial cho hàng tiêu đề
    title_font = Font(name='Arial', bold=True)
    for cell in ws[1]:  # ws[1] tương ứng với hàng đầu tiên
        cell.font = title_font

    # Ghi các liên kết vào cột A, bắt đầu từ hàng số 2 và thiết lập font
    for idx, link in enumerate(links, start=2):  # Bắt đầu từ hàng 2
        ws[f'A{idx}'] = link  # Ghi vào cột A
        ws[f'A{idx}'].font = Font(name='Arial')  # Thiết lập font chữ Arial cho các liên kết
    
    # Lưu file Excel vào bộ nhớ tạm
    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return excel_file
