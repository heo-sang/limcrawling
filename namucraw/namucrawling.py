import requests 
import json
import html
import re
from bs4 import BeautifulSoup 

url = "https://namu.wiki/w/%EC%9D%B4%EC%83%81(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"

response = requests.get(url)

if response.status_code == 200:
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'lxml')
    personality_base = soup.select_one('#app > div > div.k\+RfjiMA > div.tZQDPien > div > div._8cLLQQqW > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)')
    temp = personality_base



    


    
    content_list = []
    for content in temp(text=True):
       if content.strip():  # content가 공백이 아닌 경우에만 추가
        content_list.append(content.strip() + '\n')
    result = ''.join(content_list)
    print(result)
    with open("t2.html", "w", encoding='utf8') as file:
      file.write(result) 
    with open("output2.html", "w", encoding='utf8') as file:
      #file.write(str(temp)) # html 형식
      file.write(temp.text) # content만 남기기

    

    pattern = re.compile(r'.*display:inline.*display:none.*')
    for element in temp.find_all():
      attrs = element.attrs
      if 'style' not in attrs : continue
      if (pattern.match(attrs['style']) 
          or 'display:inline' not in attrs['style'] and 'display:none' in attrs['style']):
          element.clear()
          element.decompose()


    
    print()
    content_list = []
    for content in temp(text=True):
       if content.strip():  # content가 공백이 아닌 경우에만 추가
        content_list.append(content.strip() + '\n')
    result = ''.join(content_list)
    print(result)
    with open("t1.html", "w", encoding='utf8') as file:
      file.write(result) 
    with open("yisang_seven_html.html", "w", encoding='utf8') as file:
      file.write(str(temp.prettify())) # html 형식
      #file.write(temp.text) # content만 남기기
    

else : 
    print(response.status_code)