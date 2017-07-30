import requests
import re
from requests.exceptions import RequestException
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parser_one_page(html):
    pattern=re.compile('<img src="(.*?)".*?>.*?<h2>(.*?)</h2>.*?<div.*?>(\d+)</div>.*?<span>(.*?)</span>.*?<i class="number">(\d+)'
                       +'</i>(.*?)</span>.*?<i class="number">(\d+)</i>(.*?)</a>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'image':item[0],
            'nickname':item[1],
            'age':item[2],
            'content':item[3],
            'like':item[4]+item[5],
            'comment':item[6]+item[7]
        }

def write_to_file(item):
        with open('results2.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(item,ensure_ascii=False)+'\n')
            f.close()

def main(page):
    url='https://www.qiushibaike.com/hot/page/' + str(page)
    html=get_one_page(url)
#    print(html)
    for item in parser_one_page(html):
#        print(item)
        write_to_file(item)

if __name__=='__main__':
    for i in range(1,14):
        main(i)
#     pool=Pool()
#     pool.map(main,[i*1 for i in range(14)])