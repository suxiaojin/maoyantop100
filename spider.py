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
    pattern= re.compile('<dd>.*?boadr-index.*?(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                       +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                        +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    items= re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'immage':item[1],
            'title':item[2],
            'actor':item[3].string()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(connect):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(connect,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url='http://maoyan.com/board/4?'
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to__file(item)

if __name__=='__main__':
    main()