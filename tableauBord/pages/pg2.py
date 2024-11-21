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
query = "SELECT * from `tunnels-dirif.rapports_visites.VisiteIssuesFt0` "
rows=client.query(query).result()
rowsTab=[list(row) for row in rows]
df=pd.DataFrame(rowsTab).drop_duplicates()
df.columns=['OT','CodeEx','Tatouage','Agent','jour','Horodate']
df['Tatouage']=df['Tatouage'].str.strip()
df['Horodate']=df['Horodate'].str[:16]
df['dt']=  pd.to_datetime(df['Horodate'],format='%Y-%m-%d %H:%M')
df['date']= (df['dt']-pd.Timedelta(hours=12)).dt.strftime('%d-%m')

controleIS=pd.read_csv('https://raw.githubusercontent.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/refs/heads/master/Simulations/controleVB_IS.csv').iloc[:,:-1]
controleIS.columns=['codePC', 'tPC', 'codeRC', 'tRC']
query = "SELECT * from `tunnels-dirif.rapports_visites.lstRC0` "
rows=client.query(query).result()
rowsTab=[list(row) for row in rows]
lstRC=pd.DataFrame(rowsTab).drop_duplicates()
lstRC.columns=['ind','PC','RC','Com']
lstRC['ind']=lstRC['ind'].astype(int)

def detailIssue(iss,notes):
    visIs=df[df['CodeEx']==iss].sort_values('dt')
    if len(visIs)==0:
        return html.Div(html.H3('Aucun rapport, choisir une issue !')) 
    lstRcIs=lstRC.join(visIs,on='ind',how='inner')
    lstRcIs=lstRcIs.join(controleIS.set_index(['codePC','codeRC'])[['tPC','tRC']],on=['PC','RC']).sort_values(['Horodate','PC'])
    lstRcIs=lstRcIs[['CodeEx','Horodate','tPC','tRC','Com','Agent']]
    if len(notes)==0 :
         maxR=1
    else:
        maxR=max(notes)+1
    lstRcIs=lstRcIs[lstRcIs['tRC'].str[0].astype(int)<maxR]
    return   dash_table.DataTable(
    data=lstRcIs.to_dict(orient='records'),
    columns=[{'id': c, 'name': c} for c in lstRcIs.columns],
        style_cell_conditional=[
        {'if': {'column_id': 'CodeEx'}, 'width': '7%'},
        {'if': {'column_id': 'Agent'}, 'width': '7%'},
        ],
       style_data={   'whiteSpace': 'normal',   'height': 'auto',        'width': '30px',   'maxWidth': '100px', 'minWidth': '10px' },
    )

layout = dbc.Container([
        html.P("""Choisir une fermeture et une issues pour afficher le détail des rapports 
                  """, 
        style={'marginLeft': 90,'marginRight': 150, 'marginTop': 0}),        
        dbc.Row([
            dbc.Col(html.Label('PCTT:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='PC-dropdown2',
            options=[{'label': k, 'value': k} for k in PCs] ,
            value='PCO'
            ), width=2),  
            dbc.Col(html.Label('Fermeture:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Ferm-dropdown2',
            options=pcFrDict['PCO'] ,
            value='A14&NEU-Y'
            ), width=2),  
            dbc.Col(html.Label('Issue:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Dropdown(
            id='Iss-dropdown2',
            options=frIsDict['A14&NEU-Y'] ,
            value='IS101'
            ), width=2),  
            dbc.Col(html.Label('Notes:', style={'textAlign': 'center' }), width=1),
            dbc.Col(dcc.Checklist([1,2],  [1,2],inline=True,id='notes'), width=2),            
        ], 
        justify='center', align='center'),    
        dbc.Row(  [
            dbc.Col( id='display-Tabl2', children=  html.Div(children=[detailIssue('IS101',[1,2])])   ),
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

@callback( Output('display-Tabl2', 'children'),
    Input('Iss-dropdown2', 'value'),
    Input('notes', 'value'),
    prevent_initial_callbacks=True)  #
def tab(iss,notes):
    return  html.Div(children=[detailIssue(iss,notes)]) 


