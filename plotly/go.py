import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv')

# print(df.head())

index_vals = df['class'].astype('category').cat.codes

fig = go.Figure(data = go.Splom(
    dimensions = [dict(label = 'sepal length',
                        values = df['sepal length']),
                  dict(label = 'sepal width',
                        values = df['sepal width']),
                  dict(label = 'petal length',
                        values = df['sepal length']),
                  dict(label = 'petal width',
                        values = df['petal width'])],
                text = df['class'],
                marker = dict(color=index_vals,
                              showscale = False,
                              line_color = 'white',
                              line_width = 0.5)
))

fig.update_layout(
    title = 'Iris Data Set',
    dragmode = 'select',
    width = 600,
    height = 600,
    hovermode = 'closest',
)

fig.show()

