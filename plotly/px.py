import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv')

# print(df.head())

fig =  px.scatter_matrix(df, dimensions = ["sepal width", "sepal length", "petal width", "petal length"])
fig.show()
