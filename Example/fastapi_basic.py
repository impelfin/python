from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def healthChek():
    return "OK"

@app.get('/hello')
def Hello():
    return "Hello World~!!"

@app.post('/random')
@app.get('/random')
def random(max=None):
    import random

    if max is None:
        max = 10
    else:
        max = int(max)
    random_v = random.randint(1, max)

    return random_v
