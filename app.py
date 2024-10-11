from flask import Flask, request, render_template
import re

app = Flask(__name__)

# Hàm lọc các liên kết từ văn bản
def extract_links(text):
    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)
    return links

# Hàm thay thế liên kết trong văn bản
def replace_links(text, original_links, replacement_links):
    for i, link in enumerate(original_links):
        if i < len(replacement_links) and replacement_links[i]:
            text = text.replace(link, replacement_links[i])
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    links = []
    replaced_text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        
        if 'filter_links' in request.form:  # Khi nhấn nút "Lọc liên kết"
            links = extract_links(text)
        
        if 'replace_links' in request.form:  # Khi nhấn nút "Thay liên kết"
            links = extract_links(text)
            replacement_links = request.form.getlist("replacement_link")
            replaced_text = replace_links(text, links, replacement_links)
    
    return render_template("index.html", text=text, links=links, replaced_text=replaced_text)

if __name__ == "__main__":
    app.run(debug=True)
