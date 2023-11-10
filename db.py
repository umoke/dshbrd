import dash
from dash import html, dash_table
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data/visitors.csv')

data_table = dash_table.DataTable(
    data=df.to_dict('records')
)

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта'),
    data_table
])

if __name__ == '__main__':
    app.run_server(debug=True)