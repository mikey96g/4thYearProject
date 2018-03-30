import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Event
import plotly
import pyodbc
import pandas as pd
import plotly.graph_objs as go
from collections import deque


#Database Access
# cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
#                               ';Server=tcp:year4bitcoin.database.windows.net,1433;'
#                               'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
#                               'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

sentiment_colors = {-1:"#EE6055",
                    -0.5:"#FDE74C",
                     0:"#FFE6AC",
                     0.5:"#D0F2DF",
                     1:"#9CEC5B",}


# app_colors = {
#     'background': '#0C0F0A',
#     'text': '#FFFFFF',
#     'sentiment-plot':'#41EAD4',
#     'volume-bar':'#FBFC74',
#     'someothercolor':'#FF206E',
# }

app = dash.Dash(__name__)
app.layout = html.Div(
    [


     html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph', animate=False), className='col s12 m6 l6'),
                                         html.Div(dcc.Graph(id='historical-graph', animate=False),
                                                  className='col s12 m6 l6')]),
html.Button('Predict Next Result', id='my-button'),


        dcc.Interval(
            id='graph-update',
            interval=60000
        ),
    ]
)


#@app.callback(Output(...), [Input('my-button', 'n_clicks')])
#def on_click(number_of_times_button_has_clicked):
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                          ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                          'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    sql = "Select * from dbo.SentimentValues Order BY  dateS ,timeS  DESC"
    df = pd.read_sql(sql, cnxn)

    X = df.timeS.values[-20:]
    Y = df.sentVal.values[-20:]

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

@app.callback(Output('historical-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                          ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                          'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
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
            close=list(close_data)
            #name='Scatter',
            #mode='lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                title="CandleSticky")}

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)