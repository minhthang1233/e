from flask import Flask, request, render_template, send_file
import re
import openpyxl
from openpyxl import Workbook
import io

app = Flask(__name__)

# Hàm để trích xuất các liên kết từ văn bản
def extract_links(text):
    pattern = r'(https?://[^\s]+)'
    links = re.findall(pattern, text)
    return links

# Hàm để tạo file Excel trong bộ nhớ
def create_excel(links):
    wb = Workbook()
    ws = wb.active
    ws.title = "Links"
    
    for idx, link in enumerate(links, start=1):
        ws[f'A{idx}'] = link
    
    # Lưu file Excel vào bộ nhớ tạm
    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return excel_file

# Route để hiển thị form
@app.route('/')
def index():
    return render_template('index.html')

# Route để xử lý form và tạo file Excel
@app.route('/extract-links', methods=['POST'])
def extract_links_route():
    text = request.form['text']
    links = extract_links(text)
    excel_file = create_excel(links)
    
    # Trả về file Excel cho người dùng
    return send_file(excel_file, as_attachment=True, download_name='links.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
