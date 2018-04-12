import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Event,Input
import plotly
import pyodbc
import pandas as pd
import plotly.graph_objs as go
from collections import deque
import datetime
#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                          ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                          'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

sentiment_colors = {-1:"#EE6055",
                    -0.5:"#FDE74C",
                     0:"#FFE6AC",
                     0.5:"#D0F2DF",
                     1:"#9CEC5B",}

all_options = {
    'Sentiment': ['Lstm', 'RNN'],
    'Multiple': ['Lstm', 'Toronto', 'Ottawa']
}
app_colors = {
    'background': '#000000',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}

app = dash.Dash(__name__)
app.layout = html.Div(
[
    html.Div(className='row',children= [html.Div(dcc.Graph(id='price-graph', animate=False), className='col s12 m8 l6')]),

    dcc.Interval(
        id='graph-update',
        interval=60000,
    ),

])



@app.callback(Output('price-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def candle_stick():

    sql2 = "Select * from dbo.BitcoinVal Order BY dateB ,dboTime DESC"
    df2 = pd.read_sql(sql2, cnxn)

    X = df2.timeDate.values[-20:]
    open_data = df2.openingPrice.values[-20:]
    close_data = df2.closePrice.values[-20:]
    low_data = df2.lowPrice.values[-20:]
    high_data = df2.highPrice.values[-20:]

    data = go.Candlestick(
        x=list(X),
        open=list(open_data),
        high=list(high_data),
        low=list(low_data),
        close=list(close_data),

            )
    rangeslider = dict(
        visible=False
    )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(rangeslider = dict(
        visible=False
    )),
                                                title="CandleStick",
                                                showlegend=False,
                                                font={'color': app_colors['text']},
                                                plot_bgcolor=app_colors['background'],
                                                paper_bgcolor=app_colors['background'],
                                                )}

if __name__ == '__main__':
    app.run_server(debug=True)
