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
    df = pd.DataFrame({
        'Liên kết gốc': links,
        'Sub_id1': [None]*len(links),
        'Sub_id2': [None]*len(links),
        'Sub_id3': [None]*len(links),
        'Sub_id4': [None]*len(links),
        'Sub_id5': [None]*len(links),
        'Liên kết chuyển đổi': [None]*len(links)  # Cột G
    })

    df.to_excel(filename, index=False)

def replace_links(text, links, replacements):
    for original, replacement in zip(links, replacements):
        text = text.replace(original, replacement)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    modified_text = ""
    original_text = ""
    
    if request.method == 'POST':
        if 'text' in request.form:
            original_text = request.form['text']
            links = extract_links(original_text)

            if links:
                # Lưu các liên kết gốc vào file Excel
                excel_file = 'links.xlsx'
                save_links_to_excel(links)

                # Gửi file Excel cho người dùng
                return send_file(excel_file, as_attachment=True)

        elif 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                file.save('uploaded_links.csv')
                # Đọc các liên kết từ file CSV đã tải lên
                df = pd.read_csv('uploaded_links.csv')
                replacements = df['Liên kết chuyển đổi'].tolist()

                # Thay thế liên kết trong văn bản gốc
                modified_text = replace_links(original_text, links, replacements)

    return render_template('index.html', modified_text=modified_text, original_text=original_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  # Lắng nghe trên cổng Render
