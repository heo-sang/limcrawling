import re
import json
import lxml
from bs4 import BeautifulSoup

sin_list = ['분노','색욕','나태','탐식','우울','오만','질투']


def skill_assignment(identity_json, skill, key, value):
  identity_json['스킬'][skill].update({key:value})

def get_value(skill_detail, target):
  try:
    return skill_detail[skill_detail.index(target)+1]
  except ValueError:
    return None 

# 해당 수감자의 인격 리스트 추출
def get_identity_list(soup) :
  pattern = re.compile(r'^s-2\.\d+\.\d')
  elements = soup.find_all(id=pattern,  href='#toc')
  return [element['id'] for element in elements]


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
  target_element = base_data.find('strong', text='서포트 패시브')

  before_support_html = ''.join(str(sibling) for sibling in target_element.parent.parent.find_previous_siblings())
  before_support_soup = BeautifulSoup(before_support_html, 'html.parser')
  identity_keyword_dict = insert_keyword(before_support_soup)

  support_html = ''.join(str(sibling) for sibling in target_element.parent.find_next_siblings())
  support_soup = BeautifulSoup(support_html, 'lxml')
  support_keyword_dict = insert_keyword(support_soup)

  for span in base_data.find_all('span'):
    if 'color' not in span.get('style', '') : continue
    span.unwrap()
  return identity_keyword_dict, support_keyword_dict

### 키워드 딕셔너리에 값 추가
def insert_keyword(soup) :
  with open('temp_data/unique_keyword.json', 'r', encoding='utf8') as f:
    unique_keyword_list = json.load(f)
  keyword_list = ['충전','호흡','출혈','파열','화상','진동','침잠']
  special_keyword_list = ['탄환','구더기','저주','못','약점 분석','광신','차원 균열'
                          ,'파열 보호','결투 선포','충전 역장','버림','탐구한 지식'
                          ,'앙갚음 대상','홍매화','흑염']
  colored_basic_keyword_list = ['마비','취약','보호','신속','속박'
                                ,'도발치','공격 레벨','방어 레벨','피해량 증가']
  
  keyword_dict = {'대표':[],'기본':[],'특별':[]}
  for span in soup.find_all('span') : 
    if 'color' not in span.get('style', '') : continue
    keyword_text = span.text
    if keyword_text in keyword_list :
      keyword_dict['대표'].append(keyword_text)
    if keyword_text in colored_basic_keyword_list :
      keyword_dict['기본'].append(keyword_text)
    if keyword_text in special_keyword_list :
      keyword_dict['특별'].append(keyword_text)
    temp_keyword = unique_keyword_list.get(keyword_text, keyword_text)
    if temp_keyword in keyword_list : 
      keyword_dict['대표'].append(temp_keyword)
  keyword_dict['대표'] = sorted(set(keyword_dict['대표']))
  keyword_dict['기본'] = sorted(set(keyword_dict['기본']))
  keyword_dict['특별'] = sorted(set(keyword_dict['특별'])) 
  return keyword_dict


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

# 패시브 텍스트 추가(서포트 패시브가 하나일 경우에만 동작)
def insert_passive_text(base_data) :
  passive_elements = base_data.find_all(style='margin-bottom:5px;padding:0px 10px;color:#ffcc99;letter-spacing:-1px;text-align:left;font-size:1.1em;background-image:linear-gradient(110deg, #996633 50%, transparent 50%, transparent 51%, #996633 51%, #996633 52%,transparent 52%, transparent 53%, #996633 53%, #996633 54%, transparent 54%, transparent 55%, #996633 55%, #996633 56%, transparent 56%)')
  for element in passive_elements[:-1] :
    element.insert(0, '패시브')

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

# 기본 정보추가
def insert_basic_info(content_list) :
  identity_json = {}
  identity_name = re.sub(r'\[\s*(.*?)\s*\]', r'\1 ', content_list[0]).strip()
  identity_json['수감자'] = identity_name.split('  ')[1]
  identity_json['인격'] = identity_name
  identity_json['동기화'] = 4
  identity_json['레벨'] = 45
  status_idx = content_list.index('스테이터스') + 1
  identity_json['체력'] = int(content_list[status_idx+1])
  speed = content_list[status_idx+2].split(' - ')
  identity_json['최저속도'] = int(speed[0])
  identity_json['최고속도'] = int(speed[1])
  identity_json['수비레벨'] = int(content_list[status_idx+3].split('(')[0])
  resistance_idx = content_list.index('내성 정보')
  identity_json['내성정보'] = {}
  identity_json['내성정보'][content_list[resistance_idx+1]] = content_list[resistance_idx+2]
  identity_json['내성정보'][content_list[resistance_idx+3]] = content_list[resistance_idx+4]
  identity_json['내성정보'][content_list[resistance_idx+5]] = content_list[resistance_idx+6]
  identity_json['소속'] = content_list[content_list.index('소속')+1]
  grade = re.sub(r'\D', '', content_list[content_list.index('인격 등급')+1])
  identity_json['등급'] = int(grade)
  identity_json['출시시기'] = content_list[content_list.index('출시 시기')+1].replace('.', '-')
  return identity_json

# 스킬 정보 추가
def insert_skill_info(content_list, identity_json, attack_type_list, sin_type_list):
  skill_idx_list = [idx for idx, value in enumerate(content_list) 
                      if value == '스킬']
  skill_idx_list.append(content_list.index('패시브'))
  skill_num = 0
  defense_skill_num = 0
  for start, end in zip(skill_idx_list[:-1], skill_idx_list[1:]):
    skill_detail = content_list[start:end]
    if '수비 유형' in skill_detail:
        defense_skill_num += 1
        skill = f'수비스킬{defense_skill_num}'
    else:
        skill_num += 1
        skill = f'공격스킬{skill_num}'
    identity_json['스킬'][skill] = {}
    ###나중에 공백 지우는 re 만들어서 일괄
    coin_cnt = skill_detail.count('코인')
    skill_assignment(identity_json, skill, '코인개수',coin_cnt)
    name_idx = coin_cnt+1
    skill_assignment(identity_json, skill, '스킬이름', skill_detail[name_idx])
    attack_level = re.sub(r'\(.*?\)', '', skill_detail[name_idx+1]).strip()
    skill_assignment(identity_json, skill, '공격레벨',int(attack_level))
    action_type_key = '공격 유형' if '공격 유형' in skill_detail else '수비 유형'
    action_type = get_value(skill_detail, action_type_key)
    skill_assignment(identity_json, skill, re.sub(r'\s+', '', action_type_key), action_type)
    
    sin_type = get_value(skill_detail, '죄악 속성')
    if action_type_key =='공격 유형' : 
      attack_type_list.append(action_type)
      sin_type_list.append(sin_type)
 
    skill_assignment(identity_json, skill, '죄악속성', sin_type)
    base_power = get_value(skill_detail, '스킬 위력')
    skill_assignment(identity_json, skill, '스킬위력', int(base_power))
    coin_power = re.sub(r'\D', '', get_value(skill_detail, '코인 위력'))
    skill_assignment(identity_json, skill, '코인위력', int(coin_power))
    attack_power = get_value(skill_detail, '공격 가중치')
    if attack_power == '-' : attack_power = '1'
    skill_assignment(identity_json, skill, '공격가중치', int(attack_power))
    ### 코인별효과
    insert_coin_action(skill_detail, skill, identity_json)




# 코인별효과 추가
def insert_coin_action(skill_detail, skill , identity_json) :
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

# 패시브 정보 추가
def insert_passive_info(content_list, identity_json) : 
  passive_idx_list =[]
  passive_num = 0
  for idx, value in enumerate(content_list) :
    if value=='패시브' : passive_idx_list.append(idx)
  passive_idx_list.append(content_list.index('서포트 패시브'))
  del passive_idx_list[0]
  for start, end in zip(passive_idx_list[:-1], passive_idx_list[1:]):
    passive_detail = content_list[start:end]
    passive_num +=1
    identity_json['패시브'][passive_num] = {}
    identity_json['패시브'][passive_num]['이름'] = passive_detail[1]
    if passive_detail[2] in sin_list :
      identity_json['패시브'][passive_num]['죄악'] = passive_detail[2]
      condition = passive_detail[3].split(' ')
      identity_json['패시브'][passive_num].update({
          '수량': int(condition[0]),
          '조건': condition[1]
      })
      identity_json['패시브'][passive_num]['내용'] = passive_detail[4:]
    else :
      identity_json['패시브'][passive_num]['내용'] = passive_detail[2:]
# 서포트 패시브 정보 추가
def insert_support_passive_info(content_list, identity_json) :
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

def change_sin_by_affiliation(affiliation, identity_keyword_dict) :
  if affiliation == '약지' :
    identity_keyword_dict['대표'] = ['출혈']