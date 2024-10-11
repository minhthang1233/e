from flask import Flask, request, render_template, send_file, redirect, url_for
import re
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Định nghĩa đường dẫn lưu file CSV đã upload
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_links(text):
    # Sử dụng biểu thức chính quy để tìm các liên kết
    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)
    return links

def replace_links(text, replacements):
    # Thay thế các liên kết trong văn bản dựa trên file CSV
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    replaced_text = None  # Để lưu trữ văn bản sau khi thay thế
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Đọc file CSV
            df = pd.read_csv(filepath)
            if 'Liên kết gốc' in df.columns and 'Liên kết thay thế' in df.columns:
                # Tạo từ điển liên kết gốc và liên kết thay thế
                replacements = dict(zip(df['Liên kết gốc'], df['Liên kết thay thế']))

                # Lấy văn bản từ form
                text = request.form["text"]
                # Lọc và thay thế các liên kết
                replaced_text = replace_links(text, replacements)

    return render_template("index.html", replaced_text=replaced_text)

if __name__ == "__main__":
    app.run(debug=True)
