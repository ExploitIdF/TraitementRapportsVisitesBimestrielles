import dash,os,flask
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime,timedelta
import gunicorn   
import plotly.graph_objects as go
from google.cloud import bigquery
from  fonctions import litRC,litVisite,pcFrDict
dash.register_page(__name__,name='Dates Visites Niches',order=1)


VisiteNichesFt=litVisite('VisiteNichesFt')

VisiteNichesFt=VisiteNichesFt[VisiteNichesFt['faitLocal'].astype(int).astype(bool)]


PCs=list(pcFrDict.keys())

frTa=VisiteNichesFt[[ 'Fermeture','Tatouage']].drop_duplicates()
frTa['Tatouage']=frTa['Tatouage']+'$'
frTa=frTa.groupby('Fermeture')['Tatouage'].sum().str[:-1]
frTa=frTa.str.split('$')
FERMs=frTa.index
frTa=list(frTa)
frTaDict={FERMs[i]:frTa[i] for i in range(len(frTa)) }

def foncTable(ferm):
    dff=VisiteNichesFt[VisiteNichesFt['Tatouage'].isin(frTaDict[ferm])].copy()
    if len(dff)==0:
        return html.Div(html.H3('Aucun rapport reçu pour cette fermeture !')) 
    isDt=dff[['CodeEx','date','dt']].drop_duplicates().sort_values('dt')
    isDt['date']=isDt['date']+'  -  '
    isDt=isDt.groupby('CodeEx')['date'].sum().str[:-5].reset_index()
    return   dash_table.DataTable(
    data=isDt.to_dict(orient='records'),
    columns=[{'id': c, 'name': n} for (c,n) in [('CodeEx','Niches'),('date','Dates')]],
        style_cell_conditional=[
        {'if': {'column_id': 'CodeEx'}, 'width': '20%'},
                {'if': {'column_id': 'date'}, 'width': '80%'},
        ],

        style_data={   'whiteSpace': 'normal',   'height': 'auto',         'width': '40px',   'maxWidth': '100px', 'minWidth': '10px' },
    )


layout = dbc.Container([
        html.P("""Choisir une fermeture pour afficher l'ensemble des issues correspondantes et 
        les dates des visites bimestrielles pour lesquelles un rapport a été reçu.
                  """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col(html.Label('PCTT:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='PC-dropdown',
            options=[{'label': k, 'value': k} for k in PCs] ,
            value='PCO'
            ), width=3),  
            dbc.Col(html.Label('Fermeture:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Ferm-dropdownN',
            options=pcFrDict['PCO'] ,
            value='A14&NEU-Y'
            ), width=3),  
                   ]),    
  
        dbc.Row(  [
            dbc.Col( id='display-FermN', children=  html.Div(children=[foncTable('A14&NEU-Y')])   ),
        ]),  
])

@callback( Output('Ferm-dropdownN', "options"),
    Input('PC-dropdown', 'value'),prevent_initial_callbacks=True)  #,prevent_initial_callbacks=True
def optionsFerm(pc):
    return pcFrDict[pc]

@callback( Output('display-FermN', 'children'),
    Input('Ferm-dropdownN', 'value'),prevent_initial_callbacks=True)  #
def tab(ferm):
    return  html.Div(children=[foncTable(ferm)]) 


