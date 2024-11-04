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
dash.register_page(__name__,name='Détails par issue',order=1)
          
issues=pd.read_csv('https://exploitidf.github.io/IssuesTunnels/_downloads/caee2520ef1721f8437118adc2284ddf/issuesFermetures.csv')#'CodeEx', 'PC', 'Tatouage', 'triCode', 'Fermeture'
pcFr=issues[[ 'PC', 'Fermeture']].drop_duplicates().copy()
pcFr['Fermeture']=pcFr['Fermeture']+'$'
pcFr=pcFr.groupby('PC')['Fermeture'].sum().str[:-1]
pcFr=pcFr.str.split('$')
PCs=pcFr.index
pcFr=list(pcFr)
pcFrDict={PCs[i]:pcFr[i] for i in range(4) }

frIs=issues[[ 'Fermeture','CodeEx']].drop_duplicates().copy()
frIs['CodeEx']=frIs['CodeEx']+'$'
frIs=frIs.groupby('Fermeture')['CodeEx'].sum().str[:-1]
frIs=frIs.str.split('$')
frIsDict={frIs.index[i]:list(frIs)[i] for i in range(len(frIs)) }

frTa=issues[[ 'Fermeture','Tatouage']].drop_duplicates()
frTa['Tatouage']=frTa['Tatouage']+'$'
frTa=frTa.groupby('Fermeture')['Tatouage'].sum().str[:-1]
frTa=frTa.str.split('$')
FERMs=frTa.index
frTa=list(frTa)
frTaDict={FERMs[i]:frTa[i] for i in range(len(frTa)) }
# 	
client = bigquery.Client('tunnels-dirif')
query = "SELECT * from `tunnels-dirif.rapports_visites.VisiteIssuesFt` "
rows=client.query(query).result()
rowsTab=[list(row) for row in rows]
df=pd.DataFrame(rowsTab).drop_duplicates()
df.columns=['OT','CodeEx','Tatouage','Agent','Horodate']
df['Tatouage']=df['Tatouage'].str.strip()
df['Horodate']=df['Horodate'].str[:16]
df['dt']=  pd.to_datetime(df['Horodate'],format='%Y-%m-%d %H:%M')
df['date']= (df['dt']-pd.Timedelta(hours=12)).dt.strftime('%d-%m')

def foncTable(ferm):
    dff=df[df['Tatouage'].isin(frTaDict[ferm])].copy()
    if len(dff)==0:
        return html.Div(html.H3('Aucun rapport reçu pour cette fermeture !')) 
    isDt=dff[['CodeEx','date']].drop_duplicates()
    isDt['date']=isDt['date']+'$'
    isDt=isDt.groupby('CodeEx')['date'].sum().str[:-1].str.replace('$','  -  ').reset_index()
    return   dash_table.DataTable(
    data=isDt.to_dict(orient='records'),
    columns=[{'id': c, 'name': c} for c in isDt.columns],
        style_data={   'whiteSpace': 'normal',   'height': 'auto',   
        'width': '40px',   'maxWidth': '100px', 'minWidth': '10px' },
    )


layout = dbc.Container([
        html.H2("""Tb Pg1  
                  """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('PCTT:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='PC-dropdown2',
            options=[{'label': k, 'value': k} for k in PCs] ,
            value='PCO'
            ), width=3),  
         ]),    
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('Fermeture:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Ferm-dropdown2',
            options=pcFrDict['PCO'] ,
            value='A14&NEU-Y'
            ), width=3),  
        ]),
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('Issue:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Iss-dropdown2',
            options=frIsDict['A14&NEU-Y'] ,
            value='IS101'
            ), width=3),  
        ]),    
        dbc.Row(  [
            dbc.Col( id='display-Ferm2', children=  html.Div(children=[foncTable('A14&NEU-Y')])   ),
        ]),  
])

@callback( Output('Ferm-dropdown2', "options"),
    Input('PC-dropdown2', 'value'),prevent_initial_callbacks=True)  #,prevent_initial_callbacks=True
def optionsFerm(pc):
    return pcFrDict[pc]
@callback( Output('Iss-dropdown2', "options"),
    Input('Ferm-dropdown2', 'value'),prevent_initial_callbacks=True)  #,prevent_initial_callbacks=True
def optionsFerm(ferm):
    return frIsDict[ferm]

@callback( Output('display-Ferm2', 'children'),
    Input('Ferm-dropdown2', 'value'),prevent_initial_callbacks=True)  #
def tab(ferm):
    return  html.Div(children=[foncTable(ferm)]) 


