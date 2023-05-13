import requests
import json
import pandas as pd
from datetime import datetime

serviceKey = 'B%2FNiJnYmkZV1%2FK7ulvZI4MoSXvCTDfNAd0Snw%2Bk6g4%2BbMk1LoGVhd75DJahjv4K35Cr9jh9RX0j%2BM89grKBYsw%3D%3D'

url = 'http://apis.data.go.kr/1352000/ODMS_COVID_02/callCovid02Api'

today = datetime.today().strftime("%Y%m%d")

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

list = dict['items']
print(type(list))
print(list)
print('-' * 50)

# list to dict
items_dict = {key : value for key, value in enumerate(list)}
print(type(items_dict))
print(items_dict)
print('-' * 50)

items = items_dict[0]
print(type(items))
print(items)
print('-' * 50)

df = pd.DataFrame(items, index=[0]).rename(index={0:'result'}).T
print(type(df))
print(df)
print('-' * 50)

data = df.loc[['gPntCnt', 'hPntCnt', 'accExamCnt', 'statusDt'],:]
print(type(data))
print(data)
print('-' * 50)

