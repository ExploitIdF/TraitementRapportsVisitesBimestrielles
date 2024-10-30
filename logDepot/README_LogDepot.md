# LogDepot
241030 

Copie du repertoire initiale pour faire une variante.

Enregistrement dans BigQuery des dépôts.

`cd ~/TraitementRapportsVisitesBimestrielles/logDepot`

Commande spécifique :
```
gcloud functions deploy LogDepot \
--gen2 \
--runtime=python312 \
--region=europe-west1 \
--source=. \
--entry-point=logdepot \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=issues-secours"
```





