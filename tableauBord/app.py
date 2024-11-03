# ../.venv/Scripts\activate.ps1
# pip install -r requirements.txt

import dash,os
from flask import Flask, redirect
from dash import dcc,dash_table,html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

server = Flask(__name__)
@server.route('/')
def index_redirect():
    return redirect('/pg1')

app = dash.Dash(    __name__,    server=server, routes_pathname_prefix='/',
          external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.title = "Tableau Rapport VB"

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(  dcc.Link(f"{page['name']}", href=page["relative_path"]) , width=4)        
         for page in dash.page_registry.values()],
            justify='center', align='center')
    ]),
    dash.page_container
], style={"width": "500px"},)

if __name__ == '__main__':
   app.run_server(debug=True)

