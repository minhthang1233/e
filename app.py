from flask import Flask, request, render_template, send_file
import re
import pandas as pd
import os

app = Flask(__name__)

def extract_links(text):
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, text)
    return links

def save_links_to_excel(links, filename='links.xlsx'):
    df = pd.DataFrame(links, columns=['Links'])
    df.to_excel(filename, index=False)

def replace_links(text, links, replacements):
    for original, replacement in zip(links, replacements):
        text = text.replace(original, replacement)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    modified_text = ""
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
            links = extract_links(text)

            if links:
                # Lưu các liên kết gốc vào file Excel
                excel_file = 'links.xlsx'
                save_links_to_excel(links)

                # Gửi file Excel cho người dùng
                return send_file(excel_file, as_attachment=True)

        elif 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.xlsx'):
                file.save('uploaded_links.xlsx')
                # Đọc các liên kết từ file Excel đã tải lên
                df = pd.read_excel('uploaded_links.xlsx')
                replacements = df['Links'].tolist()

                # Lấy văn bản cũ
                original_text = request.form.get('original_text', '')
                links = extract_links(original_text)
                modified_text = replace_links(original_text, links, replacements)

    return render_template('index.html', modified_text=modified_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
