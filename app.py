from flask import Flask, request, render_template
import re
import pandas as pd
import os

app = Flask(__name__)

# Hàm lọc các liên kết từ văn bản
def extract_links(text):
    url_pattern = r'(https?://[^\s]+)'
    links = re.findall(url_pattern, text)
    return links

# Hàm thay thế các liên kết trong văn bản
def replace_links(text, links, replacements):
    for i, link in enumerate(links):
        if i < len(replacements):
            text = text.replace(link, replacements[i])
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_links = []
    replaced_text = ""
    
    if request.method == "POST":
        if "text" in request.form:
            text = request.form["text"]
            extracted_links = extract_links(text)

            # Khi người dùng nhập vào các liên kết thay thế
            if "replace_links" in request.form:
                replacements = request.form["replace_links"].splitlines()
                replaced_text = replace_links(text, extracted_links, replacements)

        # Xóa văn bản nếu người dùng yêu cầu
        if "clear" in request.form:
            text = ""
            extracted_links = []

    return render_template("index.html", extracted_links=extracted_links, replaced_text=replaced_text)

if __name__ == "__main__":
    app.run(debug=True)
