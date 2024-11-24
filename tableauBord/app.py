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
app.title = "Tableau Rapport Visites Bimestrielles"

app.layout = html.Div(dbc.Container( [
        dbc.Row([
            dbc.Col(  dcc.Link(f"{page['name']}", href=page["relative_path"]) , width=2)        
         for page in dash.page_registry.values()],
            justify='center', align='center'),
         dbc.Row([
            dbc.Col(  dash.page_container , width=8)        
        ],
            justify='center', align='center'),           
    
], fluid=True))

if __name__ == '__main__':
   app.run_server(debug=True)

