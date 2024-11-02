# Simulation des rapports
Dans ce répertoire, on a simulé des rapports pour vérifier la pertinence des spécifications et mettre au point les outils de traitement et de visualisation des résultats.   
On utilise un notebbok Jupyter : `rapportVBIS.ipynb`
Des explications sont incorporées dans le notebook.  

On génère la totalité des rapports pour l'année 2024 que l'on enregistre dans un répertoire local (24-3).   
On charge les rapports dans un bucket Google Storage en ometttant de manière aléatoire certains rapport ou certaines fermetures.  
> On n'a seulement traité VBIS


Pour authentifier auprès de google Cloud les programmes qui tournent localement dans Jupyter :  
`gcloud auth application-default login`



