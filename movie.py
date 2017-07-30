import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
def get_one_pag(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parser_one_page(html):
    pattern = re.compile('<img data-src="(.*?)" />.*?data-val.*?>(.*?)</a>.*?stonefont">(.*?)</span>(.*?)</div>', re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'url':item[0],
            'title':item[1],
            'like':item[2]
        }
def write_to_file(item):
    with open('results1.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url='http://maoyan.com/films?showType=2&offset=' + str(offset)
    html=get_one_pag(url)
    for item in parser_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
#    for i in range(9):
#        main(i*30)
    pool=Pool()
    pool.map(main,[i*10 for i in range(9)])