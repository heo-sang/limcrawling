import re
import json
import lxml
from bs4 import BeautifulSoup



# 가려진 영역 제거
def remove_hidden_area (base_data) :
  pattern = re.compile(r'.*display:inline.*display:none.*')
  for element in base_data.find_all():
    attrs = element.attrs
    if 'style' not in attrs : continue
    if (pattern.match(attrs['style']) 
        or 'display:inline' not in attrs['style'] and 'display:none' in attrs['style']):
      element.clear()
      element.decompose()

# 사용하지 않는 영역 제거
def remove_unused_data(identity_data) :
  start = identity_data.index('티켓 인사말')
  end = identity_data.index('스킬')
  del identity_data[start:end]
  panic_start = identity_data.index('패닉 유형')
  del identity_data[panic_start:]
  
# 호흡같은 의미있는 값 찾고 해당 태그 지우기
def find_keywords(base_data) :
  with open('temp_data/unique_keyword.json', 'r', encoding='utf8') as f:
    unique_keyword_list = json.load(f)
  keyword_list = ['충전','호흡','출혈','파열','화상','진동','침잠']
  
  identity_keywords = []
  for span in base_data.find_all('span') : 
    if 'color' not in span.get('style', '') : continue
    temp_text = unique_keyword_list.get(span.text, span.text)
    if(temp_text in keyword_list) : 
      identity_keywords.append(temp_text)
    span.unwrap()
  return identity_keywords

# 스킬, 코인, 죄악, 코인별효과 이미지 텍스트화
def image_to_text(base_data) :
  sin_list = ['분노','색욕','나태','탐식','우울','오만','질투']
  for element in base_data.find_all('img'):
    attrs = element.attrs
    if 'UI' in attrs['alt'] : 
      sin_name = next((sin for sin in sin_list 
                       if sin in attrs['alt']), None)
      if (sin_name and
          element.parent.parent.parent.get_text().strip() != sin_name) :
        element.insert(0,sin_name)
    if '범용스킬' in attrs['alt'] : 
      element.insert(0, '스킬')
    if "림버스컴퍼니 코인" == attrs['alt'] :
      element.insert(0, '코인')
    for num in range(1, 9):
      if (attrs['alt'] == f'림버스컴퍼니 {num}') :
        element.insert(0, f'{num}코인')    

# 특정 개행 제거
def remove_whitespace(base_data):
  remove_newline = re.sub(r'>(\n)', r'>PLACEHOLDER', str(base_data))
  remove_newline = remove_newline.replace('\n', ' ')
  remove_newline = remove_newline.replace('PLACEHOLDER', '\n')
  return BeautifulSoup(remove_newline, 'lxml').find()

# bs4에서 텍스트만 추출한 리스트 생성        
def html_to_list(base_data):
  content_list = []
  for content in base_data(text=True):
    if content.strip():  # content가 공백이 아닌 경우에만 추가
      content_list.append(content.strip())
  return content_list

# 코인별효과 추가
def coin_action(skill_detail, skill , identity_json) :
  identity_json['스킬'][skill]['코인별효과']={}
  coin_action_list = skill_detail[skill_detail.index('[ 코인별 효과 ]'):]


  coin_action_idx_list = [0]
  pattern = re.compile(r'^[1-9]코인$')
  coin_action_idx_list = [idx for idx, value in enumerate(coin_action_list) 
                          if pattern.match(value)]
  coin_action_idx_list = [0] + coin_action_idx_list + [len(coin_action_list)]
  for start, end in zip(coin_action_idx_list[:-1], coin_action_idx_list[1:]):
    coin_num = re.sub(r'\D', '', coin_action_list[start]) or '0'
    identity_json['스킬'][skill]['코인별효과'][coin_num] = coin_action_list[start+1:end]
  