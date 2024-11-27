# Formulaire pour saisir le rapport de visite

On fait une application qui permet de choisir l'une des 4 options de rapport :
* Visite bimestrielle d'issue
* Visite bimestrielle de niche
* Maintenance annuelle d'issue
* Maintenance annuelle de niche

Les points de contrôle présentés correspondent au choix qui a été fait.

Cela permet de visualiser les choix de réponse mais le choix du site et  l'enregistrement des données reste à programmer.


```
cd ~/TraitementRapportsVisitesBimestrielles/formulaireVisite

gcloud run deploy formulaire-visite  --source . --platform managed   --region europe-west1  --allow-unauthenticated
```
