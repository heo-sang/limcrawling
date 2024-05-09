f = open('./persnality_text_copy.html', 'r', encoding='utf-8')
base_text = f.read()  

# 인격 동기화부터 흐트러짐 구간까지 + 패닉유형 이후
start = base_text.find('티켓 인사말')
end = base_text.find('흐트러짐 구간')+6
for index, char_value in enumerate(base_text[end+1:], start=end+1):
  if not char_value.isdigit() and char_value != '%' :
    end = index
    break
panic_idx = base_text.find("패닉 유형")
base_text = base_text = base_text[:start] + base_text[end:panic_idx]

with open("sample_text.txt", "w", encoding='utf8') as file:
  file.write(base_text) # content만 남기기

f = open('./yisang_seven_html.html', 'r', encoding='utf-8')
base_text = f.read()  


# style 속성에 display:inline이 있는 엘리먼트 삭제
for element in base_text.find_all():
    if 'style' not in element.attrs : continue
    if'display:inline' in element.attrs['style']:
        element.clear()  # 자식 엘리먼트 제거
        element.decompose()  # 해당 엘리먼트 삭제


with open("sample_text.txt", "w", encoding='utf8') as file:
  file.write(base_text) # content만 남기기




f.close()