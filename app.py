<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extractor and Replace Links</title>
    <style>
        textarea {
            width: 100%;
            height: 100px;
        }
        .scrollable {
            height: 100px;
            overflow-y: scroll;
            width: 100%;
        }
    </style>
</head>
<body>
    <h1>Nhập văn bản để lọc và thay thế liên kết</h1>

    <form method="post">
        <h3>Văn bản</h3>
        <textarea name="text" placeholder="Nhập văn bản chứa liên kết vào đây...">{{ request.form.get('text', '') }}</textarea><br>
        
        <h3>Các liên kết lọc được</h3>
        <div class="scrollable">
            {% for link in extracted_links %}
                <p>{{ link }}</p>
            {% endfor %}
        </div><br>
        
        <h3>Nhập liên kết thay thế (mỗi liên kết một dòng)</h3>
        <textarea name="replace_links" placeholder="Nhập các liên kết thay thế..."></textarea><br>

        <button type="submit">Lọc liên kết</button>
        <button type="submit" name="clear">Xóa văn bản</button><br><br>
    </form>

    {% if replaced_text
