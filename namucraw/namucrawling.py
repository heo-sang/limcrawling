import requests 
import json
import html
import re
from bs4 import BeautifulSoup 


def skill_assignment(identity_json, skill, key, value):
  identity_json['스킬'][skill].update({key:value})

def get_value(skill_detail, target):
  try:
    return skill_detail[skill_detail.index(target)+1]
  except ValueError:
    return None 

url = "https://namu.wiki/w/%EC%9D%B4%EC%83%81(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"

#response = requests.get(url)

#if response.status_code == 200:
if True:
    f = open('./yisang.html', 'r', encoding='utf-8')
    html = f.read()  
    #html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'lxml')
    
    # 정보 바로 위 h4 값
    # tag = '#app > div > div.b0NjyPyV.rI1isyJ3 > div > div.ttkkkc5W > div > div.aKmVSIsT > div > div:nth-child(2) > div > div > h4:nth-child(15)'
    #태그 가변값임
    tag = '#app > div > div.CQbbVsrT.mgXk5wry > div > div.w69W06PT > div > div.hyj23f9g > div > div:nth-child(2) > div > div > div:nth-child(26) > div:nth-child(1)'
    identity_base = soup.select_one(tag)
    temp = identity_base
    
    temp = (
       soup.find(id="s-2.3.2", href='#toc')
       .parent
       .find_next_sibling()
       .find('div')
    )

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
          
    ### 스킬, 코인, 코인별행동 추가
    for element in temp.find_all('img'):
      attrs = element.attrs
      #임시로 이름은 고민좀
      if '범용스킬' in attrs['alt'] : 
        element.insert(0, '스킬')
      if "림버스컴퍼니 코인" == attrs['alt'] :
        element.insert(0, '코인')
      for num in range(1, 9):
        if (attrs['alt'] == f'림버스컴퍼니 {num}') :
          element.insert(0, f'{num}코인') #이름 변경 예정


    ### 개행 제거
    remove_newline = re.sub(r'>(\n)', r'>PLACEHOLDER', str(temp))
    remove_newline = remove_newline.replace('\n', ' ')
    remove_newline = remove_newline.replace('PLACEHOLDER', '\n')
    temp =  BeautifulSoup(remove_newline, 'html.parser')


    ### 리스트 형태로 변경
    content_list = []
    for content in temp(text=True):
       if content.strip():  # content가 공백이 아닌 경우에만 추가
        content_list.append(content.strip())

    ### test
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
    identity_json['수비 레벨'] = int(content_list[status_idx+3].split('(')[0])
    resistance_idx = content_list.index('내성 정보')
    identity_json[content_list[resistance_idx+1]] = content_list[resistance_idx+2]
    identity_json[content_list[resistance_idx+3]] = content_list[resistance_idx+4]
    identity_json[content_list[resistance_idx+5]] = content_list[resistance_idx+6]


    ### 기본정보
    identity_json['소속'] = content_list[content_list.index('소속')+1]
    grade = re.sub(r'\D', '', content_list[content_list.index('인격 등급')+1])
    identity_json['등급'] = int(grade)
    identity_json['출시시기'] = content_list[content_list.index('출시 시기')+1].replace('.', '-')



    ### 세력리스트 이거 db같은데 중복안되게 저장하고 이미지랑 연결하면 좋을듯
    faction_list = ['엄지','검지','중지','약지','소지',
                    '하나','츠바이','트레스','시','섕크','리우','세븐','에잇','제뱌찌','디에치','외우피',
                    '검계','피쿼드호','워더링하이츠'
                    ] 
    
    ### 이미지 저장하는 코드 작성예정



    ### 스킬

    identity_json['스킬'] = {}
    skill_idx_list =[]
    skill_num = 0
    for idx, value in enumerate(content_list) :
      if value=='스킬' : skill_idx_list.append(idx)
    skill_idx_list.append(content_list.index('패시브'))
    for idx, value in enumerate(skill_idx_list[:-1]) : 
      start = skill_idx_list[idx]
      end = skill_idx_list[idx+1]
      skill=''
      skill_detail = content_list[start:end]
      if '수비 유형' in skill_detail :
        skill = '수비스킬'
      else :
        skill_num+=1
        skill = f'공격스킬{skill_num}'
      identity_json['스킬'][skill]={}

      ###나중에 공백 지우는 re 만들어서 일괄
      coin_cnt = skill_detail.count('코인')
      skill_assignment(identity_json, skill, '코인개수',coin_cnt)
      name_idx = coin_cnt+1
      skill_assignment(identity_json, skill, '스킬이름', skill_detail[name_idx])
      attack_level = re.sub(r'\(.*?\)', '', skill_detail[name_idx+1]).strip()
      skill_assignment(identity_json, skill, '공격레벨',int(attack_level))

      action_type_key = ''
      if '공격 유형' in skill_detail :
        action_type_key = '공격 유형'
      elif '수비 유형' in skill_detail :
        action_type_key = '수비 유형'
      action_type = get_value(skill_detail, action_type_key)
      action_type_key = re.sub(r'\s+', '', action_type_key)
      skill_assignment(identity_json, skill, action_type_key, action_type)
      sin_type = get_value(skill_detail, '죄악 속성')
      skill_assignment(identity_json, skill, '죄악속성', sin_type)
      base_power = get_value(skill_detail, '스킬 위력')
      skill_assignment(identity_json, skill, '스킬위력', int(base_power))
      coin_power = re.sub(r'\D', '', get_value(skill_detail, '코인 위력'))
      skill_assignment(identity_json, skill, '코인위력', int(coin_power))
      attack_power = get_value(skill_detail, '공격 가중치')
      if attack_power == '-' : attack_power = '1'
      skill_assignment(identity_json, skill, '공격가중치', int(attack_power))

      
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
      print(f'{start} {end}')

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
    ### [사용시], [적중시]  이런거, [~]로 <span style="color:색 에서 거르면 될듯
    
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
    with open("t1.html", "w", encoding='utf8') as file:
      file.write(result) 
    with open("yisang_seven_html.html", "w", encoding='utf8') as file:
      file.write(str(temp.prettify())) # html 형식
      #file.write(temp.text) # content만 남기기
    

else : 
    print(response.status_code)
