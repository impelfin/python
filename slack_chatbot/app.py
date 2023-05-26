import requests
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
import os

app = FastAPI ( )

myToken = "xoxb-5031215990885-5326230725923-E5atoH2O6kn4uhxFJbwezKTT"
channelName = "#project"

@app.get(path='/')
async def health_check():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

@app.post(path='/sendchat')
async def sendChat(text:str):
    post_message(myToken,channelName,text)
    return {f'message:{text}'} 

@app.post(path='/sendhook')
async def sendHook(text:str):
    webhookToken = 'https://hooks.slack.com/services/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'
    cmd = "curl -X POST -H " 
    cmd += "'Content-type: application/json' --data "
    cmd += "'{" + '"text"' + ":" + '"' + text + '"' + "}' "
    cmd += webhookToken
    os.system(cmd)
    return cmd

