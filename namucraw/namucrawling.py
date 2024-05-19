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
    # 정보 바로 위 h4 값
    # tag = '#app > div > div.b0NjyPyV.rI1isyJ3 > div > div.ttkkkc5W > div > div.aKmVSIsT > div > div:nth-child(2) > div > div > h4:nth-child(15)'
    #태그 가변값임
    tag = '#app > div > div.CQbbVsrT.mgXk5wry > div > div.w69W06PT > div > div.hyj23f9g > div > div:nth-child(2) > div > div > div:nth-child(26) > div:nth-child(1)'
    identity_base = soup.select_one(tag)
    temp = identity_base

# 특정 조건을 만족하는 요소 찾기 (예: id가 "target"인 요소)
# target_element = soup.find(id="target")

# # 셀렉터 값을 생성하는 함수
# def get_css_selector(element):
#     path = []
#     while element:
#         siblings = element.find_previous_siblings(element.name)
#         index = len(siblings)
#         path.append(f"{element.name}:nth-of-type({index + 1})")
#         element = element.parent
#         if element.name == '[document]':
#             break
#     return ' > '.join(path[::-1])

# # 셀렉터 값 가져오기
# selector = get_css_selector(target_element)
# print(selector)

    ### 안보이는 영역 제거
    pattern = re.compile(r'.*display:inline.*display:none.*')
    for element in temp.find_all():
      attrs = element.attrs
      if 'style' not in attrs : continue
      if (pattern.match(attrs['style']) 
          or 'display:inline' not in attrs['style'] and 'display:none' in attrs['style']):
          element.clear()
          element.decompose()


    ### 호흡같은 의미있는 값 따로 개행되는 거 지우기
    color_spans = [span for span in temp.find_all('span') if 'color' in span.get('style', '')]
    for span in color_spans:
        span.unwrap()


    ### 죄악 img 태그에 content 추가
    sin_list = ['분노','색욕','나태','탐식','우울','오만','질투']
    for element in temp.find_all('img'):
      attrs = element.attrs
      # if element.name == 'img': # img 태그 찾는방법
      if 'UI' not in attrs['alt'] : continue
      for sin in sin_list:
        if sin not in attrs['alt'] : continue
        if element.parent.parent.parent.get_text().strip() == sin : continue
        element.insert(0,sin)
          
    ### 스킬 추가
    for element in temp.find_all('img'):
      attrs = element.attrs
      if '범용스킬' not in attrs['alt'] : continue
      element.insert(0,'스킬') #임시로 이름은 고민좀


    ### 합이후 코인별 행동 추가
    for element in temp.find_all('img'):
      attrs = element.attrs 
      for coin in range(1,9):
        if ('alt' in attrs and attrs['alt'] == '림버스컴퍼니 '+ str(coin)) :
          element.insert(0,str(coin) + '코인') #이름 변경 예정

    ### 개행 제거
    remove_newline = re.sub(r'>(\n)', r'>PLACEHOLDER', str(temp))
    remove_newline = remove_newline.replace('\n', ' ')
    remove_newline = remove_newline.replace('PLACEHOLDER', '\n')
    temp =  BeautifulSoup(remove_newline, 'html.parser')


    ### 리스트 형태로 변경
    content_list = []
    for content in temp(text=True):
       print(content)
       if content.strip():  # content가 공백이 아닌 경우에만 추가
        content_list.append(content.strip())


    ### 안 사용하는 영역 제거
    start = content_list.index('티켓 인사말')
    end = content_list.index('스킬') # 바뀔수도
    del content_list[start:end]
    panic_start = content_list.index('패닉 유형')
    del content_list[panic_start:]
    
    
    ### json 파일 제작과정
    identity_json = {}


    identity_name = re.sub(r'\[\s*(.*?)\s*\]', r'\1 ', content_list[0]).strip()
    identity_json['수감자'] = identity_name.split('  ')[1]
    identity_json['인격'] = identity_name
    identity_json['동기화'] = 4
    identity_json['레벨'] = 45

    ### 스테이터스
    status_idx = content_list.index('스테이터스') + 1
    identity_json['체력'] = int(content_list[status_idx+1])
    speed = content_list[status_idx+2].split(' - ')
    identity_json['최저속도'] = int(speed[0])
    identity_json['최고속도'] = int(speed[1])
    identity_json['수비레벨'] = int(content_list[status_idx+3].split('(')[0])
    

    ### 세력리스트 이거 db같은데 중복안되게 저장하고 이미지랑 연결하면 좋을듯
    faction_list = ['엄지','검지','중지','약지','소지',
                    '하나','츠바이','트레스','시','섕크','리우','세븐','에잇','제뱌찌','디에치','외우피',
                    '검계','피쿼드호','워더링하이츠'
                    ] 
    
    ### 이미지 저장하는 코드 작성예정


    ### 패시브
    passive_idx = content_list.index('패시브') + 1
    identity_json['패시브'] = {
        '이름': content_list[passive_idx],
        '죄악': content_list[passive_idx + 1]
    }
    condition = content_list[passive_idx + 2].split(' ')
    identity_json['패시브'].update({
        '수량': int(condition[0]),
        '조건': condition[1]
    })
    ###  패시브 여러개인 경우 고려예정
    identity_json['패시브']['내용'] = content_list[passive_idx + 3:]


    ### 서포트 패시브
    support_passive_idx = content_list.index('서포트 패시브') + 1
    identity_json['서포트 패시브'] = {
        '이름': content_list[support_passive_idx],
        '죄악': content_list[support_passive_idx + 1]
    }
    condition = content_list[support_passive_idx + 2].split(' ')
    identity_json['서포트 패시브'].update({
        '수량': int(condition[0]),
        '조건': condition[1]
    })
    identity_json['서포트 패시브']['내용'] = content_list[support_passive_idx + 3:]
    
    buff_list = ['합 위력']
    debuff_list = []
    keyword_list = ['충전','호흡','출혈','파열','화상','진동','침잠']

    ### 본국검술 같은거도 어딘가에 저장해서 다 정리해야될듯
    ### keyword 검출 
    temp_keywords = []
    for item in identity_json['서포트 패시브']['내용']:
      for keyword in keyword_list:
        if keyword not in item: continue
        temp_keywords.append(keyword)
    temp_keywords = sorted(set(temp_keywords))
    
    identity_json['서포트 키워드'] = temp_keywords


    with open('data.json', 'w', encoding='utf-8') as f:
       json.dump(identity_json, f, ensure_ascii=False, indent=4)

    
    result = '\n'.join(content_list)
    #print(result)
    with open("t1.html", "w", encoding='utf8') as file:
      file.write(result) 
    with open("yisang_seven_html.html", "w", encoding='utf8') as file:
      file.write(str(temp.prettify())) # html 형식
      #file.write(temp.text) # content만 남기기
    

else : 
    print(response.status_code)