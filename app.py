from flask import Flask, request, render_template, send_file
import re
import pandas as pd
import os

app = Flask(__name__)

def extract_links(text):
    link_pattern = r'(https?://[^\s]+)'
    links = re.findall(link_pattern, text)
    return links

def replace_links(text, links, replacements):
    for original, replacement in zip(links, replacements):
        text = text.replace(original, replacement)
    return text

def save_links_to_excel(links, filename='links.xlsx'):
    df = pd.DataFrame(links, columns=['Links'])
    df.to_excel(filename, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        replacements = request.form['replacements'].strip().split('\n')

        links = extract_links(text)
        if links:
            # Thay thế các liên kết theo thứ tự
            modified_text = replace_links(text, links, replacements)

            # Lưu các liên kết gốc vào file Excel
            excel_file = 'links.xlsx'
            save_links_to_excel(links)

            # Gửi file Excel cho người dùng
            return send_file(excel_file, as_attachment=True)

        else:
            return "Không tìm thấy liên kết nào trong văn bản."
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
