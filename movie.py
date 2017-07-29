import requests
from requests.exceptions import RequestException
import re
import json

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parser_one_page(html):
    pattern= re.compile('<dd>.*?<img data-src="(.*?)"/>.*?data-val.*?>(.*?)</a>.*?stonefont">(.*?)</span>(.*?)</div>',re.S)
    items= re.findall(pattern,html)
    for item in items:
        yield {
            'image':item[0],
            'title':item[1],
            'like':item[2]+item[3]
        }

def write_to_file(item):
    with open('result11.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
        f.close()
def main():
    url='http://maoyan.com/films?showType=2'
    html=get_one_page(url)
    for item in parser_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
    main()
