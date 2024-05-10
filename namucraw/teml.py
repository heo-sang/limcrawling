from bs4 import BeautifulSoup

# HTML 코드 예시 (변수로 받아온 것이라 가정합니다)
# html_content = """
# <html>
# <head>
# <title>HTML 예시</title>
# </head>
# <body>
# <div>
#   <p>부모 1</p>
#   <div>
#     <p>부모 2</p>
#     <div>
#       <p>부모 3</p>
#       <div>
#         <p>부모 4</p>
#         <div>
#           <p>부모 5</p>
#           <div>
#             <p>asdf</p> <!-- 여기서부터 5번째 부모를 삭제할 것입니다 -->
#           </div>
#         </div>
#       </div>
#     </div>
#   </div>
# </div>
# </body>
# </html>
# """

# # BeautifulSoup 객체 생성
# soup = BeautifulSoup(html_content, 'html.parser')

# # "asdf"가 포함된 요소 찾기
# target_element = soup.find(text="asdf").parent

# # 5번째 부모 요소 찾기
# for _ in range(5):
#     target_element = target_element.parent

# # 찾은 부모 요소 삭제
# target_element.decompose()

# # 결과 출력
# print(soup.prettify())
from bs4 import BeautifulSoup

# 예시 HTML 코드
html_content = """
<html>
<head>
<title>HTML 예시</title>
</head>
<body>
<div data-v-04926762="" style="width:100%;margin:0px -10px;text-align:left;vertical-align:top;display:inline-block;display:none">
  <p>첫 번째 문단</p>
</div>
<div data-v-04926762="" style="width:100%;margin:0px -10px;text-align:left;vertical-align:top;display:none;display:inline">
  <p>두 번째 문단</p>
</div>
</body>
</html>
"""
import re
# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

pattern = re.compile(r'.*display:inline.*display:none.*')

# display:none이 display:inline 뒤에 오는 경우는 삭제하고 반대의 경우는 남김
for element in soup.find_all():
    if 'style' in element.attrs:
      if pattern.match(element.attrs['style']) :
        element.clear()
        element.decompose()  # display:none이 display:inline 뒤에 오는 경우는 삭제
# 결과 출력
print(soup.prettify())

from bs4 import BeautifulSoup

# 예시 HTML 코드
html_content = """
<html>
<head>
<title>HTML 예시</title>
</head>
<body>
<img src="image1.jpg" alt="이미지 1">
<img src="image2.jpg" alt="이미지 2">
<div>
  <img alt="림버스탐식UI" data-v-04926762="" height="100%" src="//i.namu.wiki/i/H7uPKycqvAx5nDBg4AwAuBR2aqEeppQzvb8wINs-0vI4N23X0RV_hD2jdxtoqNQ6gUzJbSrz8mer9IZgsHWJPQ.webp"/>
</div>
</body>
</html>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

sin_list = ['분노','색욕','나태','탐식','우울','오만','질투']
for element in soup.find_all('img'):
  attrs = element.attrs
  for sin in sin_list:
    if sin not in attrs['alt'] : continue
    print(sin) 

img_tags = soup.find_all('img')

# 각 이미지 태그에 content 추가하기
for img_tag in img_tags:
    img_tag.insert(0, "1234")