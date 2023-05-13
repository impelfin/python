from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def Hello():
    str = "Hello World~!!"
    return str

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
