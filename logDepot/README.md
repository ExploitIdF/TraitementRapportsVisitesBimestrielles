# LogDepot  - Enregistrement dans BigQuery des dépôts de rapports dans Google storage.
241030 
Function déclenchée par le dépot d'un rapport

On enregistre l'heure du déport pour la comparer à l'horodatage déclaratifde l'enregistrement du dépot

`cd ~/TraitementRapportsVisitesBimestrielles/logDepot`

Commande spécifique :
```
gcloud functions deploy LogDepot --gen2 --runtime=python312 --region=europe-west1 --source=. --entry-point=logdepot --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" --trigger-event-filters="bucket=issues-secours"
```






