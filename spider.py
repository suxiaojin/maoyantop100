import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile

    items=re.findall(pattern,html)
    print(items)

def main():
    url='http://maoyan.com/board/4?'
    html=get_one_page(url)
    print(html)
    parse_one_page(html)

if __name__=='__main__':
    main()