from flask import Flask, request, render_template, send_file
import re
import pandas as pd
import os

app = Flask(__name__)

def extract_links(text):
    # Sử dụng biểu thức chính quy để tìm các liên kết
    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)
    return links

def replace_links(text, replacements):
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    modified_text = ""
    if request.method == "POST":
        text = request.form["text"]
        
        # Nếu có file CSV được tải lên
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
                
                # Giả sử cột A chứa các liên kết gốc và cột G chứa các liên kết thay thế
                replacements = dict(zip(df.iloc[:, 0], df.iloc[:, 6]))

                # Thay thế các liên kết trong văn bản
                modified_text = replace_links(text, replacements)
        
        # Lấy các liên kết từ văn bản đã nhập
        links = extract_links(text)

        if links:
            # Tạo DataFrame với các cột tiêu đề
            data = {
                "Liên kết gốc": links,
                "Sub_id1": [None] * len(links),
                "Sub_id2": [None] * len(links),
                "Sub_id3": [None] * len(links),
                "Sub_id4": [None] * len(links),
                "Sub_id5": [None] * len(links)
            }
            df = pd.DataFrame(data)

            # Lưu DataFrame vào file Excel
            filename = "extracted_links.xlsx"
            df.to_excel(filename, index=False)

            # Tải file Excel về
            return send_file(filename, as_attachment=True)
    
    return render_template("index.html", modified_text=modified_text)

if __name__ == "__main__":
    app.run(debug=True)
