# Tableau de bord des rapports de visites
Dans ce répertoire, on traite d'une application qui permet de consulter les rapports qui ont été déposés par le titulaire (ou simulés en phase de développement).

### Lien vers l'application (données simulées)
https://tableau-bord-rapports-visites-987317455394.europe-west1.run.app/



## Développement
Il s'agit d'une application Dash dont les sources sont dans ce répertoire :
cd ~/TraitementRapportsVisitesBimestrielles/tableauBord
Pour tester l'application localement, il faut être dans le projet tunnel du compte exploit.dirif
entrer sur le terminal : 
python3 app.py

Pour le déploiement :
cd ~/TraitementRapportsVisitesBimestrielles/tableauBord
gcloud run deploy tableau-bord-rapports-visites  --source . --platform managed   --region europe-west1  --allow-unauthenticated

En cas de difficulté, entrer `gcloud info` pour vérifier le compte et le projet de la configuration active.

  
