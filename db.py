import dash
from dash import html, dash_table, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

df = pd.read_csv('data/visitors.csv')

dropdown = dcc.Dropdown(
    id='dropdown',
    options=[
        {'label': 'Visitors', 'value': 'Visitors'},
        {'label': 'Pageviews', 'value': 'Pageviews'},
        {'label': 'Bounce Rate', 'value': 'BounceRate'},
        {'label': 'Average Session Duration', 'value': 'AvgSessionDuration'}
    ],
    value='Visitors'
)

time_series_chart = dcc.Graph(
    id='time-series-chart'
)

pie_chart = dcc.Graph(
    id='pie-chart'
)

histogram = dcc.Graph(
    id='histogram'
)

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта'),
    html.P('Выберите категорию для анализа:'),
    dropdown,
    time_series_chart,
    pie_chart,
    histogram,
])


@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('dropdown', 'value')]
)
def int_time_series(selected_metric):
    fig = px.line(df,x='Date',y=selected_metric,title=f'График временного ряда для {selected_metric}',labels={'Date': 'Дата', selected_metric: selected_metric})
    return fig


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('dropdown', 'value')]
)
def int_pie_chart(selected_metric):
    fig = px.pie(df,names='Date',values=selected_metric,title=f'Круговая диаграмма для {selected_metric}',labels={'Date': 'Дата', selected_metric: selected_metric})
    return fig


@app.callback(
    Output('histogram', 'figure'),
    [Input('dropdown', 'value')]
)
def int_histogram(selected_metric):
    fig = px.bar(df, x='Date', y=selected_metric, title=f'Гистограмма для {selected_metric}', labels={'Date': 'Дата', selected_metric: selected_metric})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)