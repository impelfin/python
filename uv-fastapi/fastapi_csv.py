from fastapi import FastAPI
import pandas as pd
import uvicorn

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getcsv')
def get_csv():
    csv_file = 'data.csv'

    df = pd.read_csv(csv_file)
    dict_data = df.to_dict()

    return dict_data
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
