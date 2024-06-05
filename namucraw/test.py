from identity_crawling import *
from data_processing import *

sinner_list = ["이상","파우스트","돈키호테","로슈","뫼르소","홍루"
               ,"히스클리프","이스마엘","로쟈","싱클레어","오티스","그레고르"]
sinner = sinner_list[4]
identity_id = 's-2.3.4'

url = f"https://namu.wiki/w/{sinner}(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
response = requests.get(url)
if response.status_code != 200:
  url = f"https://namu.wiki/w/{sinner}/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
  response = requests.get(url)
html = response.content.decode('utf-8','replace') 
soup = BeautifulSoup(html, 'html.parser')
identity_crawling(soup, sinner, identity_id)

