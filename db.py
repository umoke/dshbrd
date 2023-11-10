import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import io
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта', style={'textAlign': 'center'}),

    dcc.Upload(
        id='upload-data',
        children=html.Button('Загрузить файл CSV'),
        multiple=False,
    ),

    html.P('Выберите категорию для анализа:'),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Количество посетителей за день', 'value': 'Visitors'},
            {'label': 'Количество новых посетителей за день', 'value': 'NewVisitors'},
            {'label': 'Количество просмотренных страниц за день', 'value': 'Pageviews'},
            {'label': 'Процент посетителей, которые ушли с сайта после просмотра только одной страницы',
             'value': 'BounceRate'},
            {'label': 'Средняя продолжительность сессии в минутах', 'value': 'AvgSessionDuration'}
        ],
        value='Visitors',
    ),

    html.P('Выберите период анализа:'),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2023-01-01',
        end_date=None
    ),

    dcc.Graph(
        id='time-series-chart',
    ),

    dcc.Graph(
        id='pie-chart',
    ),

    dcc.Graph(
        id='histogram',
    ),
])


@app.callback(
    [Output('time-series-chart', 'figure'), Output('pie-chart', 'figure'), Output('histogram', 'figure')],
    [Input('upload-data', 'contents'), Input('dropdown', 'value'), Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_charts(contents, selected_metric, start_date, end_date):
    if contents is None:
        return {}, {}, {}

    content_type, content_string = contents.split(',')
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))

    filtered_data = decoded[(decoded['Date'] >= start_date) & (decoded['Date'] <= end_date)]

    time_series_fig = px.line(filtered_data, x='Date', y=selected_metric,
                              title=f'График временного ряда для {selected_metric}',
                              labels={'Date': 'Дата', selected_metric: selected_metric})

    pie_chart_fig = px.pie(filtered_data,names='Date', values=selected_metric,
                           title=f'Круговая диаграмма для {selected_metric}',
                           labels={'Date': 'Дата', selected_metric: selected_metric})

    histogram_fig = px.bar(filtered_data, x='Date', y=selected_metric,
                           title=f'Гистограмма для {selected_metric}',
                           labels={'Date': 'Дата', selected_metric: selected_metric})

    return time_series_fig, pie_chart_fig, histogram_fig


if __name__ == '__main__':
    app.run_server(debug=True)