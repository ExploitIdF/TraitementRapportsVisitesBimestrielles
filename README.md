# Rapports des visites et de la maintenance des issues et niches
Ce **repository** contient la documentation des outils de gestion des rapports qui seront produits par le prestataire du marché Batiment 
dont l'attribution est prévue début 2025. Les exigences sont inscrite dans le DCE du marché. 
On trouve ici des informations complémentaires et qui pourront être mises à jour tout au long de l'execution du marché.

Les tunnels comportent environ 290 issues et 430 niches que l'on a regroupées dans environ 30 **fermetures** 
qui sont des ensembles d'issues et de niches bénéficiant de fermetures nocturnes simultanées et 
qui peuvent donc être visitées la même nuit.

La liste de référence des issues est disponible ici : 
https://raw.githubusercontent.com/ExploitIdF/IssuesTunnels/main/_static/issuesTunnelsDIRIF.csv

La liste de référence des niches est disponible ici : 
https://raw.githubusercontent.com/ExploitIdF/IssuesTunnels/main/_static/nichesBrExPc.csv

Les correspondances entre issues et fermetures sont définies par la table suivante :
https://raw.githubusercontent.com/ExploitIdF/IssuesTunnels/refs/heads/main/_static/issuesFermetures.csv

<mark>Les correspondances entre niches et fermetures sont définies par la table suivante :</mark>
> <mark>à compléter</mark>

Le titulaire devra réaliser chaque année 5 visites bimestrielles et 1 intervention de maintenance préventive de chaque issue et de chaque niche.
Le rapport d'une intervention de maintenance préventive est composé du rapport d'une visite bimestrielle et 
d'un complément de rapport qui concerne les actions spécifiques à cette intervention.


## Formats des fichiers à déposer
Le titulaire du marché devra mettre une application de saisie des rapports sur un terminal mobile, à disposition des agents intervenant dans les tunnels.
Les rapports seront envoyés directement depuis le terminal de l'agent sur le serveur de la DIRIF.

A ce stade, il est prévu que le serveur soit un **bucket dans Google Storage** sur lequel le titulaire disposera de droit d'écriture.
Ainsi, dans la version de développement, les fichiers peuvent être atteints par une URL du type : 
https://storage.googleapis.com/issues-secours/rapports-visites/345467-3196056.json

On distingue 4 modèles de rapports :

* rapport de la visite bimestrielle d'une issue
* rapport de la visite bimestrielle d'une niche
* complément de rapport pour la maintenance annuelle d'une issue
* complément de rapport pour la maintenance annuelle d'une niche

Les rapports sont composés de plusieurs **points de contrôle (PC)**.

Pour chaque point de contrôle, le rapport doit comporter le choix du **résultat du contrôle (RC)** parmi des options prédéfinies et 
un commentaire de l'agent sous la forme d'un texte libre. Le commentaire est obligatoire pour les résultat du contrôle qui traduisent
un défaut majeur ou mineur.

Les listes de **points de contrôle (PC)** et  **résultat du contrôle (RC)** sont :

* [Points de controles des visites bimestrielles des issues](https://raw.githubusercontent.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/refs/heads/master/controleVB_IS.csv?token=GHSAT0AAAAAACY3JSDXA2I6D3A6U5CCQCXCZZDJT2Q)
* Points de controles des visites bimestrielles des niches
* Points de controles complémentaires des interventions de maintenance des issues
* liste

Dans les fichiers les PC et RC sont identifiés par les codes à 3 caractères indiqués dans les listes.

## Contrôle et intégration des fichiers
Les contrôles qui seront effectués










