import dash
import dash_core_components as dcc
import dash_html_components as html
import pyodbc
import pandas as pd

#Database Access
cnxn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:projdata.database.windows.net,1433;Database=projData;Uid=mikey96g@projdata;Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()

sql = "Select * from dbo.SentimentValues"
sql1 = "Select * from dbo.BitcoinVal"
df = pd.read_sql(sql,cnxn)
df1 = pd.read_sql(sql1,cnxn)

app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='Sentiment Score'),

    html.Div(children='''
        Values taken every minute.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.timeS, 'y': df.sentVal, 'type': 'line'},
            ],
            'layout': {
                'title': 'Sentiment'
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)