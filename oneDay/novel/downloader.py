import requests
import faker
import urllib.parse
from bs4 import BeautifulSoup

url = 'https://www.xxbiquge.com/23_23396/'

def download(url = None):
    if url is None:
        print("URL is None")
        return
    user_agent = faker.Faker().user_agent()
    headers = {'User-Agent': user_agent}

    content = requests.get(url, headers=headers)
    content.encoding = "utf-8"

    soup = BeautifulSoup(content.text, 'html.parser', from_encoding='utf-8')

    for lst in soup.find_all(id='list'):
        if lst is None:
            break
        title = lst.find('dd').text
        for a in lst.find_all('a'):
            href = urllib.parse.urljoin(url,a.get('href'))
            title = a.text
            print(href,title)

if __name__ == '__main__':
    download(url)
