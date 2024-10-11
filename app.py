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
    for old_link, new_link in replacements.items():
        text = text.replace(old_link, new_link)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    updated_text = None

    if request.method == "POST":
        if 'action' in request.form:
            action = request.form['action']

            # Xử lý trường hợp trích xuất liên kết
            if action == "extract":
                text = request.form["text"]
                links = extract_links(text)

                if links:
                    # Tạo DataFrame để lưu các liên kết
                    data = {
                        "Liên kết gốc": links,
                        "Sub_id1": [None] * len(links),
                        "Sub_id2": [None] * len(links),
                        "Sub_id3": [None] * len(links),
                        "Sub_id4": [None] * len(links),
                        "Sub_id5": [None] * len(links)
                    }
                    df = pd.DataFrame(data)
                    filename = "extracted_links.xlsx"
                    df.to_excel(filename, index=False)

                    # Tải file Excel về
                    return send_file(filename, as_attachment=True)

            # Xử lý trường hợp tải lên file CSV
            elif action == "upload":
                if 'csv_file' in request.files:
                    csv_file = request.files['csv_file']
                    if csv_file.filename.endswith('.csv'):
                        # Đọc file CSV
                        csv_data = pd.read_csv(csv_file)
                        replacements = dict(zip(csv_data.iloc[:, 0], csv_data.iloc[:, 6]))

                        # Lấy văn bản từ input
                        text = request.form.get("text", "")
                        text = replace_links(text, replacements)
                        
                        # Cập nhật văn bản đã thay thế để hiển thị
                        updated_text = text

    return render_template("index.html", updated_text=updated_text)

if __name__ == "__main__":
    app.run(debug=True)
