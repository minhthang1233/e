from flask import Flask, request, render_template, send_file
import re
import pandas as pd

app = Flask(__name__)

# Hàm lọc liên kết từ văn bản
def extract_links(text):
    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)
    return links

# Hàm thay thế liên kết trong văn bản
def replace_links(text, original_links, replacement_links):
    for i in range(min(len(original_links), len(replacement_links))):
        if replacement_links[i]:  # Kiểm tra xem có liên kết thay thế không
            text = text.replace(original_links[i], replacement_links[i])  # Thay thế theo thứ tự
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    links = []
    replaced_text = ""
    
    if request.method == "POST":
        text = request.form.get("text", "")
        
        # Khi nhấn nút "Tạo file Excel"
        if 'create_excel' in request.form:
            links = extract_links(text)
            if links:
                # Tạo DataFrame để lưu liên kết vào file Excel
                data = {
                    "Liên kết gốc": links,
                    "Thay thế": [None] * len(links)
                }
                df = pd.DataFrame(data)
                filename = "extracted_links.xlsx"
                df.to_excel(filename, index=False)
                return send_file(filename, as_attachment=True)

        # Khi nhấn nút "Lọc liên kết"
        elif 'filter_links' in request.form:
            links = extract_links(text)
        
        # Khi nhấn nút "Thay liên kết"
        elif 'replace_links' in request.form:
            links = extract_links(text)  # Lấy các liên kết từ văn bản
            replacement_text = request.form.get("replacement_links", "")
            replacement_links = replacement_text.splitlines()  # Tách từng dòng làm từng liên kết thay thế
            replaced_text = replace_links(text, links, replacement_links)  # Thay thế liên kết
        
        # Khi nhấn nút "Xóa văn bản"
        elif 'clear_text' in request.form:
            text = ""
    
    return render_template("index.html", text=text, links=links, replaced_text=replaced_text)

if __name__ == "__main__":
    app.run(debug=True)
