import requests
import json
import pandas as pd
from datetime import datetime, timedelta

serviceKey = 'B%2FNiJnYmkZV1%2FK7ulvZI4MoSXvCTDfNAd0Snw%2Bk6g4%2BbMk1LoGVhd75DJahjv4K35Cr9jh9RX0j%2BM89grKBYsw%3D%3D'

url = 'http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'

today = (datetime.today() - timedelta(1)).strftime("%Y%m%d")

params = '?serviceKey='+ serviceKey
params += '&pageNo=1'
params += '&numOfRows=500'
params += '&apiType=JSON'
params += '&status_dt=' + str(today)

url += params

response = requests.get(url)
print(response)
print('-' * 50)

contents = response.text
print(type(contents))
print(contents)
print('-' * 50)

dict = json.loads(contents)
print(type(dict))
print(dict)
print('-' * 50)

items = dict['items'][0]
print(type(items))
print(items)
print('-' * 50)

item = ['gPntCnt', 'hPntCnt', 'accExamCnt', 'statusDt']
# vlidItem = {key: value for key, value in items.fromkeys(item).items()}
# print(vlidItem)

validItem = {}
for _ in item:
    validItem[_] = items[_]
print(validItem)