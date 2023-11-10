import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import io
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(children='Анализ данных о посещении веб-сайта'),

    dcc.Upload(
        id='upload-data',
        children=html.Button('Загрузить файл CSV'),
        multiple=False,
    ),

    html.P('Выберите категорию для анализа:'),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Visitors', 'value': 'Visitors'},
            {'label': 'Pageviews', 'value': 'Pageviews'},
            {'label': 'Bounce Rate', 'value': 'BounceRate'},
            {'label': 'Average Session Duration', 'value': 'AvgSessionDuration'}
        ],
        value='Visitors',
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
    [Input('upload-data', 'contents'), Input('dropdown', 'value')]
)
def update_charts(contents, selected_metric):
    if contents is None:
        return {}, {}, {}

    content_type, content_string = contents.split(',')
    decoded = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))

    time_series_fig = px.line(decoded,x='Date',y=selected_metric,title=f'График временного ряда для {selected_metric}',labels={'Date': 'Дата', selected_metric: selected_metric})

    pie_chart_fig = px.pie(decoded,names='Date',values=selected_metric,title=f'Круговая диаграмма для {selected_metric}',labels={'Date': 'Дата', selected_metric: selected_metric})

    histogram_fig = px.bar(decoded, x='Date', y=selected_metric, title=f'Гистограмма для {selected_metric}', labels={'Date': 'Дата', selected_metric: selected_metric})

    return time_series_fig, pie_chart_fig, histogram_fig


if __name__ == '__main__':
    app.run_server(debug=True)