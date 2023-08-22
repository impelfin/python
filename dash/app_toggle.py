import plotly.express as px
from dash import Dash, dcc, html, Input, Output

import pandas as pd

app = Dash(__name__)

# preprocess
data = pd.read_csv("./data/seoul_house.csv", encoding="UTF8")
data = data.loc[:, [
    "k-아파트명", "k-단지분류(아파트,주상복합등등)", "주소(시군구)", "주소(읍면동)", 
    "k-복도유형", "k-난방방식", "k-전체세대수", "주차대수", "좌표X", "좌표Y"]]
data.columns = ["아파트명", "단지분류", "시군구", "읍면동", "복도유형", "난방방식", "세대수", "주차대수", "좌표X", "좌표Y"]
groups = data["시군구"].unique()

# 레이아웃 정의
app.layout = html.Div(children=[
    html.H1(
        children="서울시 공동주택 아파트 정보",
        style={"textAlign": "center"}
    ),
    html.H4(
        children="시군구를 선택하세요", 
    ),
    dcc.Dropdown(
    	id="group",
        options=groups,
        value=groups[0]
    ),
    dcc.Graph(
        id="graph",
    ),
], style={"width": "90%", "margin": "auto"})

# 콜백 정의
@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="group", component_property="value"),
)
def update_graph(group):

    # 사용자가 선택한 시군구가 포함된 데이터를 필터링
    selected_data = data.loc[data["시군구"] == group]
    
    # boxplot 그래프 생성
    fig = px.box(
        selected_data, x="시군구", y="세대수"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)