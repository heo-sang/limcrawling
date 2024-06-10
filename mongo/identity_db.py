
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import glob
from pymongo.errors import DuplicateKeyError
import dotenv 
import os

dotenv.read_dotenv()
mongo_uri = os.environ.get('mongo_uri')


# MongoDB 연결 문자열
# MongoDB 클라이언트 생성
client = MongoClient(mongo_uri)
db = client['limbus_data']
collection = db['identity_detail']

### 전체 인격 저장, db에 데이터 있을 때 어떻게 하는지 관리
def identity_init():
  file_paths = []
  sinner_list = ["이상","파우스트","돈키호테","료슈","뫼르소","홍루"
                 ,"히스클리프","이스마엘","로쟈","싱클레어","오티스","그레고르"]
  for sinner in sinner_list:
    file_paths += glob.glob(f'../namucraw/json/identity/{sinner}/*.json')
  for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
      data = json.load(file)
      insert_data_with_unique_index(collection, data)


def insert_data_with_unique_index(collection, data):
    try:
        collection.insert_one(data)
        print("데이터가 삽입되었습니다.")
    except DuplicateKeyError:
        print("중복된 데이터가 존재합니다. 삽입하지 않습니다.")

# 데이터 삽입 시도
#identity_init()
#collection.delete_many({})


def add_keywords() :
  special_keywords = []
  basic_keywords = []

  file_paths = []
  sinner_list = ["이상","파우스트","돈키호테","료슈","뫼르소","홍루"
                 ,"히스클리프","이스마엘","로쟈","싱클레어","오티스","그레고르"]
  for sinner in sinner_list:
    file_paths += glob.glob(f'../namucraw/json/identity/{sinner}/*.json')
  for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
      data = json.load(file)
      keywords = data['키워드']
      support_keywords = data['키워드']
      for k in keywords['기본']:
        basic_keywords.append(k)
      for k in support_keywords['기본']:
        basic_keywords.append(k)
      for k in keywords['특별']:
        special_keywords.append(k)
      for k in support_keywords['특별']:
        special_keywords.append(k)
     
      # db['basic_keyword'].insert_one()
      # db['special_keyword'].insert_one(keywords, support_keywords)
      # db['special_keyword'].insert_one()
  special_keywords = sorted(set(special_keywords))
  basic_keywords = sorted(set(basic_keywords))
  print(special_keywords)
  print(basic_keywords)
add_keywords()