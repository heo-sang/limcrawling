from identity_crawling import *
from data_processing import *
def main():

  with open('sinners.json', 'r', encoding='utf-8') as f:
    sinner_dict = json.load(f) 
  for sinner in sinner_dict:
    url = f"https://namu.wiki/w/{sinner}(Project%20Moon%20%EC%84%B8%EA%B3%84%EA%B4%80)/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
    response = requests.get(url)
    if response.status_code != 200:
      url = f"https://namu.wiki/w/{sinner}/%EC%9D%B8%EA%B2%8C%EC%9E%84%20%EC%A0%95%EB%B3%B4"
      response = requests.get(url)
    if response.status_code != 200:
      print(response.status_code)
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'html.parser')
    identity_id_list = get_identity_list(soup)
    for identity_id in identity_id_list:
      print(f'{sinner}, {identity_id}')
      identity_crawling(soup, sinner, identity_id)
    

if __name__ == "__main__":

  main()
