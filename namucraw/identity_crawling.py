import requests 
import json
import html
import re
from bs4 import BeautifulSoup 
from data_processing import *
import os
import time


def identity_crawling(soup, sinner_name, identity_id) :
  with open('sinners.json', 'r', encoding='utf-8') as f:
    sinner_dict = json.load(f) 
  name_soup = soup.find(id=identity_id, href='#toc')
  identity_prefix = name_soup.find_next_sibling()
  identity_prefix.select_one('.wiki-edit-section').decompose()
  identity_prefix = identity_prefix.text
  if '[임시]' in identity_prefix: 
    print(f'{sinner_name} : {identity_id} 임시데이터')
    return
  identity_name = f"{identity_prefix} {sinner_name}"
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
  save_identity_image(base_data, sinner_name, identity_prefix, identity_name.replace(' ','_'))
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

  with open('./content_temp.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(content_list))

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
  
  sinner_num= sinner_dict[sinner_name]
  serial_number = get_serial_number(sinner_num,identity_json,identity_id)
  identity_json = {**serial_number, **identity_json}
  underbar_identity_name = identity_name.replace(' ','_')
  special_character = ['/', ':', '*', '?', '"', '<', '>', '|']
  for character in special_character:
    underbar_identity_name = underbar_identity_name.replace(f'{character}','_')
  num = identity_json['일련번호']
  json_path = f'./json/identity/{sinner_name}/{num}_{underbar_identity_name}.json'
  with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(identity_json, f, ensure_ascii=False, indent=2)    
