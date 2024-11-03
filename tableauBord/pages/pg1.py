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
dash.register_page(__name__,name='Rapports des visites bimestrielles',order=1)
          
issues=pd.read_csv('https://exploitidf.github.io/IssuesTunnels/_downloads/caee2520ef1721f8437118adc2284ddf/issuesFermetures.csv')#'CodeEx', 'PC', 'Tatouage', 'triCode', 'Fermeture'
pcFr=issues[[ 'PC', 'Fermeture']].drop_duplicates()
pcFr['Fermeture']=pcFr['Fermeture']+'$'
pcFr=pcFr.groupby('PC')['Fermeture'].sum().str[:-1]
pcFr=pcFr.str.split('$')
PCs=pcFr.index
pcFr=list(pcFr)
pcFrDict={PCs[i]:pcFr[i] for i in range(4) }

frTa=issues[[ 'Fermeture','Tatouage']].drop_duplicates()
frTa['Tatouage']=frTa['Tatouage']+'$'
frTa=frTa.groupby('Fermeture')['Tatouage'].sum().str[:-1]
frTa=frTa.str.split('$')
FERMs=frTa.index
frTa=list(frTa)
frTaDict={FERMs[i]:frTa[i] for i in range(len(frTa)) }

client = bigquery.Client()
table =client.dataset("rapports_visites").table("LogDepot")
query = "SELECT * from `tunnels-dirif.rapports_visites.LogDepot` "
rows=client.query(query).result()
rowsTab=[list(row) for row in rows]
df=pd.DataFrame(rowsTab).drop_duplicates()
df.columns=['Tatouage', 'HoroDate', 'Agent', 'PC0', 'CM0', 'PC1', 'CM1', 'PC2', 'CM2', 'PC3', 'CM3', 'PC4', 'CM4', 'PC5', 'CM5', 'PC6', 'CM6', 
                  'PC7', 'CM7', 'PC8', 'CM8', 'PC9', 'CM9', 'PC10', 'CM10', 'PC11', 'CM11', 'PC12', 'CM12', 'PC13', 'CM13', 'PC14', 'CM14']
df['Tatouage']=df['Tatouage'].str.strip()
df['dt']=  pd.to_datetime(df['HoroDate'],format='%Y-%m-%d %H:%M:%S')
df['date']= (df['dt']-pd.Timedelta(hours=12)).dt.strftime('%d-%m')
df=df.join(issues.set_index('Tatouage')['CodeEx'],on='Tatouage')


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
        'width': '70px',   'maxWidth': '120px', 'minWidth': '30px' },
    )


layout = html.Div([
        html.H2("""Tb Pg1  
                  """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('PCTT:', style={'text-align': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='PC-dropdown',
            options=[{'label': k, 'value': k} for k in PCs] ,
            value='PCN'
            ), width=3),  
                   ]),    

        dbc.Row([
            dbc.Col( '  ' , width=1),
            dbc.Col(html.Label('Fermeture:', style={'text-align': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Ferm-dropdown',
            options=pcFrDict['PCO'] ,
            value='A14&NEU-Y'
            ), width=3),  
                   ]),    
        dbc.Row(  [
            dbc.Col( id='display-Ferm', children=  html.Div(children=[foncTable('A14&NEU-Y')])   ),
        ]),


])

@callback( Output('Ferm-dropdown', "options"),
    Input('PC-dropdown', 'value'))  #,prevent_initial_callbacks=True
def met_a_jour(pc):
    return pcFrDict[pc]

@callback( Output('display-Ferm', 'children'),
    Input('Ferm-dropdown', 'value'))  #,prevent_initial_callbacks=True
def tab(ferm):
    return  html.Div(children=[foncTable(ferm)]) 


