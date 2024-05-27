import requests 
import json
import html
import re
from bs4 import BeautifulSoup 
from data_processing import *


url = "https://namu.wiki/w/%EC%9D%B4%EC%83%81(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
response = requests.get(url)

if response.status_code == 200:
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'lxml')
    base_data = (
       soup.find(id="s-2.3.2", href='#toc')
       .parent
       .find_next_sibling()
       .find('div')
    )

    with open('temp_data/unique_keyword.json', 'r', encoding='utf8') as f:
      unique_keyword_list = json.load(f)
    keyword_list = ['충전','호흡','출혈','파열','화상','진동','침잠']
    sin_list = ['분노','색욕','나태','탐식','우울','오만','질투']
    attack_type_list = []
    sin_type_list = []
    ### 안보이는 영역 제거
    remove_hidden_area(base_data)

    ### 호흡같은 의미있는 값 인격 키워드에 추가하고 해당 태그 지우기
    identity_keywords = find_keywords(base_data)

    ### 스킬, 코인, 죄악 이미지 텍스트화
    image_to_text(base_data)

    ### 개행 제거
    base_data = remove_whitespace(base_data)

    ### 리스트 형태로 변경
    content_list = html_to_list(base_data)

    ### 안 사용하는 영역 제거
    remove_unused_data(content_list)
    
    ### json 파일 제작과정
    identity_json = insert_basic_info(content_list)
    
    ### 이미지 저장하는 코드 작성예정



    ### 스킬

    identity_json['스킬'] = {}
    insert_skill_info(content_list, identity_json, attack_type_list, sin_type_list)

    identity_json['공격유형'] = sorted(set(attack_type_list))
    identity_json['죄악속성'] = sorted(set(sin_type_list))
    identity_json['키워드'] = sorted(set(identity_keywords))

      
    ### 스타일 이거하나당 패시브 하나 margin-bottom:5px;padding:0px 10px;color:#ffcc99;letter-spacing:-1px;text-align:left;font-size:1.1em;background-image:linear-gradient(110deg, #996633 50%, transparent 50%, transparent 51%, #996633 51%, #996633 52%,transparent 52%, transparent 53%, #996633 53%, #996633 54%, transparent 54%, transparent 55%, #996633 55%, #996633 56%, transparent 56%)
    identity_json['패시브'] = {}
    passive_idx_list =[]
    passive_num = 0
    for idx, value in enumerate(content_list) :
      if value=='패시브' : passive_idx_list.append(idx)
    passive_idx_list.append(content_list.index('서포트 패시브'))
    for idx, value in enumerate(passive_idx_list[:-1]) : 
      start =passive_idx_list[idx]
      end = passive_idx_list[idx+1]
      passive=''
      passive_detail = content_list[start:end]

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

    ### 본국검술 같은거도 어딘가에 저장해서 다 정리해야될듯
    ### [사용시], [적중시]  이런거, [~]로 <span style="color:색 에서 거르면 될듯
    
    ### keyword 검출 
    support_keywords = []
    for item in identity_json['서포트 패시브']['내용']:
      for keyword in keyword_list:
        if keyword not in item: continue
        support_keywords.append(keyword)
    support_keywords = sorted(set(support_keywords))
    
    identity_json['서포트 키워드'] = support_keywords


    with open('data.json', 'w', encoding='utf-8') as f:
       json.dump(identity_json, f, ensure_ascii=False, indent=2)

    
    result = '\n'.join(content_list)
    with open("t1.html", "w", encoding='utf8') as file:
      file.write(result) 
    with open("yisang_seven_html.html", "w", encoding='utf8') as file:
      file.write(str(base_data.prettify())) # html 형식
    

else : 
    print(response.status_code)
