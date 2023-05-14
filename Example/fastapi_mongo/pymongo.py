from asyncio import current_task
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

HOST = 'cluster0.rbwdg3a.mongodb.net'
USERNAME = 'root'
PASSWORD = '1234'

client = MongoClient(f'mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}')

db = client['test']
# db = client.mediscountDB

@app.get('/mongo')
async def get_users_in_mongo():
  collection = db['testdb']
  return list(collection.find().limit(10))