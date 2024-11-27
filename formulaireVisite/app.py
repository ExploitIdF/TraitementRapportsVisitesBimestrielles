import dash,os,pandas as pd
from flask import Flask, redirect 
from dash import dcc,dash_table,html,callback
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

server = Flask(__name__)
app = dash.Dash(    __name__,    server=server,    external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "formulaire Issues et Niches"
contr=pd.read_csv('https://raw.githubusercontent.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/refs/heads/master/_static/controlesIsNi.csv')
print(contr.iloc[:1,:7])
#contrP=pd.DataFrame(contr-store["data-frame"])
tpVisites=["Visite bimestrielle d'issue", "Visite bimestrielle de niche", "Maintenance annuelle d'issue", "Maintenance annuelle de niche"]
cdVisites=["Issue_VB","Niche_VB","Issue_IA", "Niche_IA"]
dictVisites={cdVisites[i]: tpVisites[i] for i in range(4)}

dropdownTypeVisite = dbc.DropdownMenu(
    id="dropdownTypeVisite",
    label="Type de visite", 
    children=[
        dbc.DropdownMenuItem("Visite bimestrielle d'issue",id="Issue_VB"),
        dbc.DropdownMenuItem("Visite bimestrielle de niche",id="Niche_VB"),
        dbc.DropdownMenuItem("Maintenance annuelle d'issue",id="Issue_IA"),
        dbc.DropdownMenuItem("Maintenance annuelle de niche",id="Niche_IA"),
    ],
)
def formulaire(rep):
    if len(rep)<2:
        return "zzz"
    contrP=contr[contr[rep]=='Oui']
    PCs=list(contrP['codePC'].unique())
    dicRC={pc:list(contrP[contrP['codePC']==pc]['RC'].unique()) for pc in PCs}

    return html.Div(([
                          (
                            html.Div([html.H5(contrP[contrP['codePC']==pc].iloc[0,1]),
                            dcc.Dropdown(  dicRC[pc], id='id-'+pc ),
                            
                            dcc.Input(id='comm-{}'.format(pc) ,placeholder="Commentaire ?",style={"width":"100%"}) ])
                          ) for pc in  PCs
                        ] ),
    )


app.layout = dbc.Container( [dcc.Store("contr-store"),
        dbc.Row([
            dbc.Col( html.H3("Saisie des rapports Issues & Niches"), width=6) ,   
            dbc.Col( [dropdownTypeVisite,html.Div(id="choix-rapport") ], width=6)        
         ],
            justify='center', align='center'),
        html.Hr(),
         dbc.Row([
            dbc.Col( "A", id="formulaire")        
        ],
            justify='center', align='center'),           
    ], fluid=True,style={"width":"450px"},class_name="border  border-5")

@callback([Output( "choix-rapport", "children"),Output("formulaire","children") ,Output("contr-store", "data")], 
[Input(cdV, "n_clicks") for cdV in cdVisites]) 
def choixRapport(*args):
    rep="Issue_VB"
    ctx = dash.callback_context
    rep=ctx.triggered[0]['prop_id'].split('.')[0]
    if len(rep)<3:
        rep="Issue_VB"
    return html.H5(dictVisites[rep]),formulaire(rep) ,"z"

if __name__ == '__main__':
   app.run_server(debug=True)

