<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extractor Links</title>
</head>
<body>
    <h1>Nhập văn bản để lọc liên kết</h1>
    <form method="post" enctype="multipart/form-data">
        <textarea name="text" rows="10" cols="50" placeholder="Nhập văn bản ở đây..."></textarea><br>
        <button type="submit" name="action" value="extract">OK</button>
    </form>

    <h2>Tải lên file CSV để thay thế liên kết</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="csv_file" accept=".csv" required>
        <button type="submit" name="action" value="upload">Tải lên CSV</button>
    </form>

    {% if updated_text %}
        <h3>Văn bản đã thay thế:</h3>
        <pre>{{ updated_text }}</pre>
    {% endif %}
</body>
</html>
