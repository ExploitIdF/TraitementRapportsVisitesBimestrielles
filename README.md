# Traitement des rapports de visites d'issues
Documentation : https://cloud.google.com/functions/docs/tutorials/storage 

La fonction est inscrite dans un fichier .py on a dans le même répertoire un requirements.txt


Lieu des commandes : exploit_diridf@cloudshell

Il  faut renseigner le projet avec gcloud init (project ID :tunnels-dirif)

ou bien  `gcloud config set project tunnels-dirif`



```
gcloud functions deploy python-finalize-function \
--gen2 \
--runtime=python312 \
--region=europe-west1 \
--source=. \
--entry-point=hello_gcs \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=issues-secours"
```



