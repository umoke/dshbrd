import dash
from dash import html
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data/visitors.csv')

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта'),

])

if __name__ == '__main__':
    app.run_server(debug=True)