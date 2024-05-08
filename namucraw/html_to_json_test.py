f = open('./output2.html', 'r', encoding='utf-8')
print()
base_text = f.read()  


# 인격 동기화부터 흐트러짐 구간까지 + 패닉유형 이후
start = base_text.find('티켓 인사말')
end = base_text.find('흐트러짐 구간')+6
for index, char_value in enumerate(t[end+1:], start=end+1):
  if not char_value.isdigit() and char_value != '%' :
    end = index
    break
panic_idx = base_text.find("패닉 유형")



f.close()