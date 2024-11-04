# Simulation des rapports
Dans ce répertoire, on a simulé des rapports pour vérifier la pertinence des spécifications et mettre au point les outils de traitement et de visualisation des résultats des visites bimestrielles.   
On utilise un notebbok Jupyter : `rapportVBIS.ipynb`  
https://github.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/blob/master/Simulations/rapportVBIS.ipynb

Des explications plus détaillées sont incorporées dans le notebook.  

On génère le calendrier prévisionnel des visites par fermeture et la totalité des visites programmées.  
On génère les rapports en simulant aléatoirement :

* que des visites de fermetures sont annulées ou reportées
* que des rapports sont absents

La totalité des rapports est chargée *en masse* dans  la base de donnée BigQuery  

De première visualisations sont mises en place.

On simule le dépot des rapports sur Google Storage avec une fonction déclenchée automatiquement pour les incorporer à la base de donnée BigQuery

> On n'a seulement traité VBIS

Pour authentifier auprès de google Cloud les programmes qui tournent localement dans Jupyter :  
`gcloud auth application-default login`



