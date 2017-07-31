import requests
response=requests.get('http://bizhi.zhuoku.com/2013/05/23/xiaoqingxin/xiaoqingxin021.jpg')
with open('aa.jpg','wb') as f:
    f.write(response.content)
    f.close()