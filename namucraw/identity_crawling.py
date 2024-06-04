import requests 
import json
import html
import re
from bs4 import BeautifulSoup 
from data_processing import *
import os
import time

sinner_list = ['이상','파우스트','돈키호테','로슈','뫼르소','홍루'
               ,'히스클리프','이스마엘','로쟈','싱클레어','오티스','그레고르']

# for sinner in sinner_list:
#   url = f"https://namu.wiki/w/{sinner}(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
#   response = requests.get(url)
#   if response.status_code != 200:
#     url = f"https://namu.wiki/w/{sinner}/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
#     response = requests.get(url)
#   if not os.path.exists(f'./image/identity/{sinner}'):
#       os.makedirs(f'./image/identity/{sinner}')
# start = time.time()
# time_cost = time.time()-start
url = "https://namu.wiki/w/뫼르소/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
response = requests.get(url)
if response.status_code == 200:
  html = response.content.decode('utf-8','replace') 
  soup = BeautifulSoup(html, 'html.parser')
  
  identity_id_list = get_identity_list(soup)
  name_soup = soup.find(id="s-2.3.4", href='#toc')
  identity_prefix = name_soup.find_next_sibling()
  identity_prefix.select_one('.wiki-edit-section').decompose()
  identity_prefix = identity_prefix.text
  identity_name = f"{identity_prefix} 뫼르소".replace(' ','_')
  base_data = (
     name_soup
     .parent
     .find_next_sibling()
     .find('div')
  )

  with open('temp_data/unique_keyword.json', 'r', encoding='utf8') as f:
    unique_keyword_list = json.load(f)
  
  ### 안보이는 영역 제거
  remove_hidden_area(base_data)
  ### 호흡같은 의미있는 값 인격 키워드에 추가하고 해당 태그 지우기(대표, 범용, 특별)
  identity_keyword_dict, support_keyword_dict = find_keywords(base_data)
  
  ### 이미지 저장하는 코드 작성예정
  save_identity_image(base_data, identity_prefix, identity_name)
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
  identity_json = insert_basic_info(content_list)
  
  ### 스킬
  identity_json['스킬'] = {}
  attack_type_list, sin_type_list = insert_skill_info(content_list, identity_json)
  change_sin_by_affiliation(identity_json['소속'], identity_keyword_dict)
 
  insert_passive_info(content_list, identity_json)
  ### 서포트 패시브
  insert_support_passive_info(content_list, identity_json)
  
  ### 본국검술 같은거도 어딘가에 저장해서 다 정리해야될듯
  ### [사용시], [적중시]  이런거, [~]로 <span style="color:색 에서 거르면 될듯
  ### span에서 처리해야될듯
  basic_keyword_list = ['합 위력','최종 위력','코인 위력','수비 위력'
                        ,'기본 위력','피해량 +','체력 회복']

  mentality_pattern = re.compile(r'정신력 \d+ 회복')

  ### keyword 검출 
  find_rest_keyword(identity_json, identity_keyword_dict, support_keyword_dict)
  # for item in identity_json['서포트 패시브']['내용']:
  #   for keyword in keyword_list:
  #     if keyword in item: 
  #        support_keywords.append(keyword)
      
  identity_json['공격유형'] = sorted(set(attack_type_list))
  identity_json['죄악속성'] = sorted(set(sin_type_list))
  identity_json['키워드'] = identity_keyword_dict
  identity_json['서포트 키워드'] = support_keyword_dict

  with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(identity_json, f, ensure_ascii=False, indent=2)    

    
else : 
    print(response.status_code)
