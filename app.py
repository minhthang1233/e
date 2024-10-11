from flask import Flask, request, jsonify, render_template
import urllib.parse
import requests
import os
import re

app = Flask(__name__)

# Hàm để mã hóa URL
def encode_link(link):
    base_url = link.split('?')[0]  # Lấy phần URL trước dấu hỏi
    return urllib.parse.quote(base_url, safe='')  # Mã hóa phần đó

# Hàm để giải mã liên kết rút gọn thành liên kết đầy đủ
def resolve_short_link(short_url):
    try:
        response = requests.head(short_url, allow_redirects=True)
        return response.url  # Trả về URL đầy đủ sau khi chuyển hướng
    except requests.RequestException:
        return None

@app.route('/')
def index():
    return render_template('index.html')

# Hàm xử lý kết quả khi người dùng nhập liên kết
@app.route('/generate_links', methods=['POST'])
def generate_links():
    data = request.get_json()  # Nhận dữ liệu JSON từ yêu cầu
    input_text = data.get('text')  # Lấy văn bản đầu vào

    if not input_text:
        return jsonify(error="Vui lòng cung cấp văn bản.")  # Trả về lỗi nếu không có văn bản

    # Tìm tất cả các liên kết trong văn bản
    short_links = re.findall(r'https?://(?:vn\.shp\.ee|s\.shopee\.vn)/[^\s]+', input_text)

    # Tạo một dictionary để lưu các liên kết mới
    new_links = {}
    for short_link in short_links:
        full_link = resolve_short_link(short_link)  # Giải mã liên kết rút gọn
        if full_link:
            encoded_link = encode_link(full_link)  # Mã hóa liên kết
            new_link = f"https://shope.ee/an_redir?origin_link={encoded_link}&affiliate_id=17385530062&sub_id=1review"
            new_links[short_link] = new_link

    # Thay thế các liên kết trong văn bản
    for short_link, new_link in new_links.items():
        input_text = input_text.replace(short_link, new_link)

    return jsonify(results=[input_text])  # Trả về văn bản đã thay thế dưới dạng JSON

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Sử dụng biến môi trường PORT
    app.run(host='0.0.0.0', port=port)
