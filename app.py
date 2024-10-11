from flask import Flask, render_template, request, redirect, url_for
import openpyxl

app = Flask(__name__)

# Trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý form và trả về dữ liệu
@app.route('/submit', methods=['POST'])
def submit():
    # Nhận dữ liệu từ form
    data = request.form['data']
    # Ghi dữ liệu vào tệp Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = data
    workbook.save('data.xlsx')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
