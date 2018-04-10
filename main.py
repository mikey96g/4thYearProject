import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Event,Input
import plotly
import pyodbc
import pandas as pd
import plotly.graph_objs as go
from collections import deque


#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server}'
                          ';Server=tcp:year4bitcoin.database.windows.net,1433;'
                          'Database=year4Proj;Uid=mikey96g@year4bitcoin;Pwd={Tallaght123!};'
                          'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

cursor = cnxn.cursor()
# Start the scheduler

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

sentiment_colors = {-1:"#EE6055",
                    -0.5:"#FDE74C",
                     0:"#FFE6AC",
                     0.5:"#D0F2DF",
                     1:"#9CEC5B",}


app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}
def return_prediction():
    sql = "Select TOP 1 sentTotal from dbo.SentimentValues Order BY  dateS ,timeS  DESC "
    sq = pd.read_sql(sql, cnxn)
    sq = sq.values
    sq[0]



app = dash.Dash()

app.layout = html.Div([



    html.Div(className='container-fluid', children=[html.H2('Live Bitcoin Predictions', style={'color': "#000000"})]),
    html.Hr(),
    html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph', animate=False),
                                        className='col s12 m8 l6'),
                                        html.Div(dcc.RadioItems(
                                        id='countries-dropdown',
                                        options=[{'label': k, 'value': k} for k in all_options.keys()],
                                        value='America'
    ),
                                        className='col s12 m4 ')]),
    html.Div(className='row',children=[html.Div(dcc.Graph(id='historical-graph', animate=False),
                                                 className='col s12 m8 l6'),
                                       html.Div(dcc.Graph(id='historical-graph', animate=False),
                                                 className='col s12 m8 l6')]),
    html.Hr(),
    html.Div([html.Button('Click Me', id='button'),
              html.H3(id='button-clicks'), ]),

], className='container')

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])

def update_graph_scatter():

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
@app.callback(
    Output('button-clicks', 'children'),
    [Input('button', 'n_clicks')])
def clicks(n_clicks):
    return 'The predicted value is {} '.format(return_prediction())


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})


# server = app.server # the Flask app

# if __name__ == '__main__':
#     app.run_server(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
