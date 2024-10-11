from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Xử lý dữ liệu từ form
    data = request.form.get('data')
    if data:
        # Xử lý dữ liệu ở đây (ví dụ: lưu vào cơ sở dữ liệu, xử lý thông tin, ...)
        return redirect(url_for('index'))
    return 'Data not provided', 400

if __name__ == '__main__':
    app.run(debug=True)
