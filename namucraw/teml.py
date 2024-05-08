from bs4 import BeautifulSoup

# HTML 코드 예시 (변수로 받아온 것이라 가정합니다)
html_content = """
<html>
<head>
<title>HTML 예시</title>
</head>
<body>
<div>
  <p>부모 1</p>
  <div>
    <p>부모 2</p>
    <div>
      <p>부모 3</p>
      <div>
        <p>부모 4</p>
        <div>
          <p>부모 5</p>
          <div>
            <p>asdf</p> <!-- 여기서부터 5번째 부모를 삭제할 것입니다 -->
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# "asdf"가 포함된 요소 찾기
target_element = soup.find(text="asdf").parent

# 5번째 부모 요소 찾기
for _ in range(5):
    target_element = target_element.parent

# 찾은 부모 요소 삭제
target_element.decompose()

# 결과 출력
print(soup.prettify())