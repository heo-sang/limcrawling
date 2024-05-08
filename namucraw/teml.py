from bs4 import BeautifulSoup

html_content = """
<html>
<head><title>Test HTML</title></head>
<body>
<div id="content">
    <p>This is some content.</p>
    <p>This is more content.</p>
</div>
</body>
</html>
"""

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 모든 태그를 제거하고 텍스트(content)만 추출
content = soup.get_text()

print("태그를 모두 제거한 내용:")
print(content)