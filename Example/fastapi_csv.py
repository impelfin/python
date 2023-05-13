from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get('/')
def healthChek():
    return "OK"

@app.get('/getcsv')
def get_csv():
    csv_file = 'data.csv'

    df_data = pd.read_csv(csv_file)
    dict_data = df_data.to_dict()

    return dict_data