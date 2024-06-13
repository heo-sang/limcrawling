
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import DuplicateKeyError
import dotenv 
import os


dotenv.read_dotenv()
mongo_uri = os.environ.get('mongo_uri')

# MongoDB 클라이언트 생성
client = MongoClient(mongo_uri)
db = client['limbus_data']
collection = db['identity_detail']

# 고유 인덱스 설정
collection.create_index([("일련번호", 1)], unique=True)