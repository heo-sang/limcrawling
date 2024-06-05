import requests 
import json
import html
import re
from bs4 import BeautifulSoup 
from data_processing import *
import os
import time


with open('sinners.json', 'r', encoding='utf-8') as f:
  sinner_dict = json.load(f) 
# for sinner, sinner_num in sinner_dict.items():
#   url = f"https://namu.wiki/w/{sinner}(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
#   response = requests.get(url)
#   if response.status_code != 200:
#     url = f"https://namu.wiki/w/{sinner}/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
#     response = requests.get(url)
# start = time.time()
 
url = "https://namu.wiki/w/뫼르소/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
response = requests.get(url)
if response.status_code == 200:
  html = response.content.decode('utf-8','replace') 
  soup = BeautifulSoup(html, 'html.parser')
  start = time.time()
  identity_id_list = get_identity_list(soup)
  identity_id ="s-2.3.4"
  name_soup = soup.find(id="s-2.3.4", href='#toc')
  identity_prefix = name_soup.find_next_sibling()
  identity_prefix.select_one('.wiki-edit-section').decompose()
  identity_prefix = identity_prefix.text
  identity_name = f"{identity_prefix} 뫼르소"
  base_data = (
     name_soup
     .parent
     .find_next_sibling()
     .find('div')
  )

  ### 안보이는 영역 제거
  remove_hidden_area(base_data)
  ### 호흡같은 의미있는 값 인격 키워드에 추가하고 해당 태그 지우기(대표, 범용, 특별)
  identity_keyword_dict, support_keyword_dict = find_keywords(base_data)
  
  ### 이미지 저장하는 코드 작성예정
  save_identity_image(base_data, identity_prefix, identity_name.replace(' ','_'))
  ### 스킬, 코인, 죄악 텍스트화
  image_to_text(base_data)
  ### 패시브 텍스트 추가
  insert_passive_text(base_data)
  ### 개행 제거
  base_data = remove_whitespace(base_data)
  ### 리스트 형태로 변경
  content_list = html_to_list(base_data)
  ### 안 사용하는 영역 제거
  remove_unused_data(content_list) 
  ### json 파일 제작과정
  identity_json = insert_basic_info(content_list, identity_name)
  
  ### 스킬
  identity_json['스킬'] = {}
  attack_type_list, sin_type_list = insert_skill_info(content_list, identity_json)
  change_sin_by_affiliation(identity_json['소속'], identity_keyword_dict)
 
  ### 패시브 정보
  insert_passive_info(content_list, identity_json)
  insert_support_passive_info(content_list, identity_json)
  
  ### keyword 검출 
  find_rest_keyword(identity_json, identity_keyword_dict, support_keyword_dict)
  
  identity_json['공격유형'] = sorted(set(attack_type_list))
  identity_json['죄악속성'] = sorted(set(sin_type_list))
  identity_json['키워드'] = identity_keyword_dict
  identity_json['서포트 키워드'] = support_keyword_dict

  sinner_num = '01'
  serial_number = get_serial_number(sinner_num,identity_json,identity_id)
  identity_json = {**serial_number, **identity_json}
  with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(identity_json, f, ensure_ascii=False, indent=2)    
  time_cost = time.time()-start
  print(round(time_cost,3))  
else : 
    print(response.status_code)
