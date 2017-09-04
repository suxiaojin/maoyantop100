from urllib import request
from bs4 import BeautifulSoup as bs
from urllib import request
import warnings
warnings.filterwarnings('ignore')
import jieba
import numpy
import codecs
import re
import pandas as pd
import matpl

resp=request.urlopen("https://movie.douban.com/nowplaying/nanjing/")
html_data=resp.read().decode('utf-8')
#print(html_data)
soup=bs(html_data,"html.parser")
nowplaying_movie=soup.find_all("div",id="nowplaying")
#print(nowplaying_movie)
nowplaying_movie_list=nowplaying_movie[0].find_all('li',class_='list-item')
#print(nowplaying_movie_list)
nowplaying_list=[]
for item in nowplaying_movie_list:
    nowplaying_dict={}
    nowplaying_dict['id']=item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name']=tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)
requrl=""
