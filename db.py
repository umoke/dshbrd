import dash
from dash import html, dash_table, dcc
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('data/visitors.csv')

data_table = dash_table.DataTable(
    data=df.to_dict('records')
)

dropdown = dcc.Dropdown(
)

time_series_chart = dcc.Graph(
)

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта'),
    data_table,
    dropdown,
    time_series_chart,
])

if __name__ == '__main__':
    app.run_server(debug=True)