import plotly.express as px
from dash import Dash, dcc, html

import pandas as pd

# 앱 초기화
app = Dash(__name__)

# preprocess
data = pd.read_csv("./data/seoul_house.csv", encoding="UTF8")
data = data.loc[:, [
    "k-아파트명", "k-단지분류(아파트,주상복합등등)", "주소(시군구)", "주소(읍면동)", 
    "k-복도유형", "k-난방방식", "k-전체세대수", "주차대수", "좌표X", "좌표Y"]]
data.columns = ["아파트명", "단지분류", "시군구", "읍면동", "복도유형", "난방방식", "세대수", "주차대수", "좌표X", "좌표Y"]

# 그래프 정의
fig = px.box(
    data, x="시군구", y="세대수"
)

# 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(
        children="서울시 공동주택 아파트 정보",
        style={"textAlign": "center"}
    ),
    html.H4(
        children="시군구별 세대수 분포", 
    ),
    dcc.Graph(
        id="graph",
        figure=fig
    ),
], style={"width": "90%", "margin": "auto"})

if __name__ == '__main__':
    app.run_server(debug=True)