

cd ~/TraitementRapportsVisitesBimestrielles/tableauBord
localement python3 app.py

Deploiement :
gcloud run deploy tableau-bord-rapports-visites  --source . \
  --platform managed   --region europe-west1  --allow-unauthenticated

  
