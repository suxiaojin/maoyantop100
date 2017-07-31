import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import os
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError

def get_page_index(offset,keyword):
    data={
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    url='https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parser_page_index(html):
    try:
        data=json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错',url)
        return None

def parser_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    print(title)
    image_pattern=re.compile('var gallery = (.*?);',re.S)
    result=re.search(image_pattern,html)
    if result:
        data=json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title':title,
                'images':images,
                'url':url
            }

def download_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url)
        if response.status_code==200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    html=get_page_index(offset,'街拍')
    for url in parser_page_index(html):
        html=get_page_detail(url)
        if html:
            result=parser_page_detail(html,url)
            print(result)

if __name__=='__main__':
    groups=[x*20 for x in range(1,9)]
    pool=Pool()
    pool.map(main,groups)
