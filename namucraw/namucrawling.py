import requests 
import json
import html
from bs4 import BeautifulSoup 

url = "https://namu.wiki/w/%EC%9D%B4%EC%83%81(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"

response = requests.get(url)

if response.status_code == 200:
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'html.parser')
    #title = soup.select('#app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)')
    #print(soup.select('#app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(14) > div:nth-child(1) '))
    # parent_tag = soup.find('div', {"data-v-04926762": ""})
    # parent_tag.extract()
    
    #app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)
    # programs = soup.select('div>div>div') 
    # tagtemp = soup.find_all('#app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)')
    title = soup.select_one('#app > div > div.k\+RfjiMA > div.tZQDPien > div > div._8cLLQQqW > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)')
    temp = title.text
    print(type(temp))
    temp = temp.replace(']', "]\n")
#app > div > div.k\+RfjiMA > div.tZQDPien > div > div._8cLLQQqW > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)
#app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)    #app > div > div.YjvyFted > div._0qEOfn5o > div > div.tWrauFr\+ > div > div:nth-child(2) > div > div > div:nth-child(18) > div:nth-child(1)
    with open("output2.html", "w", encoding='utf8') as file:
      file.write(temp)
else : 
  
    print(response.status_code)