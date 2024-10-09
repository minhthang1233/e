@app.route('/', methods=['GET', 'POST'])
def index():
    modified_text = ""
    original_text = ""
    links = []  # Khởi tạo links với danh sách rỗng
    
    if request.method == 'POST':
        try:
            if 'text' in request.form:
                original_text = request.form['text']
                links = extract_links(original_text)  # Gán giá trị cho links

                if links:  # Nếu có liên kết, tạo file Excel
                    excel_file = 'links.xlsx'
                    save_links_to_excel(links)
                    return send_file(excel_file, as_attachment=True)

            elif 'file' in request.files:  # Nếu người dùng tải file CSV
                file = request.files['file']
                if file and file.filename.endswith('.csv'):
                    file.save('uploaded_links.csv')  # Lưu file CSV
                    df = pd.read_csv('uploaded_links.csv')
                    replacements = df['Liên kết chuyển đổi'].tolist()
                    modified_text = replace_links(original_text, links, replacements)  # Sử dụng links ở đây

                    os.remove('uploaded_links.csv')  # Xóa file sau khi xử lý

        except Exception as e:
            logging.error("Error occurred: %s", str(e))
            return f"An error occurred: {e}", 500

    return render_template('index.html', modified_text=modified_text, original_text=original_text)
