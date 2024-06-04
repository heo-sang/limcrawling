import requests 
import json
import html
import re
from bs4 import BeautifulSoup 
from data_processing import *
import os
import time

with open('data.json','r', encoding='utf-8') as f :
  mentality_pattern = re.compile(r'.*정신력 \d+ 회복.*')
  rest_keyword_list = ['공격 가중치','화상']

  identity_json = json.load(f)



