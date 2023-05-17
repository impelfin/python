from fastapi import FastAPI
from pymongo import mongo_client
import pydantic
from bson.objectid import ObjectId

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

HOST = 'cluster0.rbwdg3a.mongodb.net'
USERNAME = 'root'
PASSWORD = '1234'

client = mongo_client.MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}')
print('Connected to Mongodb....')
# mongodb+srv://root:1234@cluster0.rbwdg3a.mongodb.net/

mydb = client['test']
mycol = mydb['testdb']

@app.get('/')
async def healthCheck():
    return "OK"

@app.get('/getmongo')
async def getMongo():
  return list(mycol.find().limit(10))

@app.get("/getuser")
async def getuser(id=None):
    if id is None:
        return "id를 입력하세요."
    result = mycol.find_one({"id":id})
    if result:
        return result
    else:
        return "검색 결과가 없습니다."

@app.get("/useradd")
async def useradd(id=None, name=None):
    if (id and name) is None:
        return "id, name을 입력하세요"
    else:
        user = dict(id=id, name=name)
        mycol.insert_one(user)
        result = mycol.find_one({"id": id})
        return result

@app.get("/userupdate")
async def userupdate(id=None, name=None):
    if (id and name) is None:
        return "id, name을 입력하세요"
    else:
        user = mycol.find_one({"id": id})
        if user:
            filter = {'id':id}
            data = {"$set":{'name':name}}
            mycol.update_one(filter, data)
            result = mycol.find_one({"id": id})
            return result
        else:
            return f"id = {id} 데이터가 존재하지 않습니다."

@app.get("/userdel")
async def userdel(id=None):
    if id is None:
        return "id를 입력하세요"
    else:
        user = mycol.find_one({"id": id})
        if user:
            mycol.delete_one({"id": id})
            return list(mycol.find().limit(10))
        else:
            return f"id = {id} 데이터가 존재하지 않습니다."