import  os 
import pandas as pd
from google.cloud import bigquery


def litRC(tbNom):
    client = bigquery.Client('tunnels-dirif')
    query = "SELECT * from `tunnels-dirif.rapports_visites." +tbNom+"`"
    rows=client.query(query).result()
    rowsTab=[list(row) for row in rows]
    lstRC=pd.DataFrame(rowsTab).drop_duplicates()
    lstRC.columns=['ind','PC','RC','Com']
    lstRC['ind']=lstRC['ind'].astype(int)
    return lstRC

def litVisite(tbNom):
    client = bigquery.Client('tunnels-dirif')
    query = "SELECT * from `tunnels-dirif.rapports_visites." +tbNom+"`"
    rows=client.query(query).result()
    rowsTab=[list(row) for row in rows]
    Visites=pd.DataFrame(rowsTab).drop_duplicates()
    Visites.columns=['OTF','CodeEx','Tatouage','Agent','jour','Horodate','Fermeture','ordreVB','faitFerm','faitLocal' ]
    Visites['dt']=  pd.to_datetime(Visites['Horodate'].str[:16],format='%Y-%m-%d %H:%M')
    Visites['date']= (Visites['dt']-pd.Timedelta(hours=12)).dt.strftime('%d-%m')
    return Visites

pcFrDict={'PCE': ['NOG-I',
  'NOG-E',
  'GMO&MOU-I',
  'GMO&MOU-E',
  'CHA-Y',
  'CHA-W',
  'BOI-Y',
  'BOI-W'],
 'PCN': ['BLN&CRN-I', 'BLN&CRN-E', 'LAN-Y', 'LAN-W', 'TAV'],
 'PCO': ['A14&NEU-Y',
  'NAN-I',
  'NAN-E',
  'A14&NEU-W',
  'SEV',
  'RUE-I',
  'RUE-E',
  'FLF-Y',
  'FLF-W',
  'BAP&SCL-Y',
  'BAP&SCL-W',
  'CHE'],
 'PCS': ['FRE&ANT-I', 'FRE&ANT-E', 'BIC&ITA-Y', 'BIC&ITA-W', 'ORL']}
