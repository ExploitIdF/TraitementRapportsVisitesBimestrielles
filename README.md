# Rapports des visites et de la maintenance des issues et niches
Ce **repository** contient la documentation des outils de gestion des rapports qui seront produits par le prestataire du marché Batiment, 
dont l'attribution est prévue début 2025. Les exigences sont inscrites dans le DCE du marché. 
On trouve ici des informations complémentaires et qui pourront être mises à jour tout au long de l'execution du marché.

Les tunnels comportent environ 290 issues et 430 niches que l'on a regroupées dans environ 30 **fermetures** 
qui sont des ensembles d'issues et de niches bénéficiant de fermetures nocturnes simultanées et 
qui peuvent donc être visitées la même nuit.

La liste de référence des issues est disponible ici : 
https://raw.githubusercontent.com/ExploitIdF/IssuesTunnels/main/_static/issuesTunnelsDIRIF.csv

La liste de référence des niches est disponible ici : 
https://raw.githubusercontent.com/ExploitIdF/IssuesTunnels/main/_static/nichesBrExPc.csv

Les correspondances entre issues et fermetures sont définies par la table suivante :
['Table des correspondances entre issues et fermetures'](https://raw.githubusercontent.com/ExploitIdF/Referentiel_Tunnels/refs/heads/main/issuesFermetures.csv)

<mark>Les correspondances entre niches et fermetures sont définies par la table suivante :</mark>
> <mark>à compléter</mark>

Le titulaire devra réaliser, chaque année, 5 visites bimestrielles et 1 intervention de maintenance préventive de chaque issue et de chaque niche.
Le rapport d'une intervention de maintenance préventive est composé du rapport d'une visite bimestrielle et 
d'un complément de rapport qui concerne les actions spécifiques à cette intervention.

## Commandes et ordres de travail
Les actions préventives de visites bimestrielles ou d'interventions de maintenance annuelle sont commandées de manière groupées par fermetures 
et elles concernent à la fois les issues et les niches. Pour les visites bimestrielles, d'une part, et pour les interventions de maintenance annuelle, d'autre part,
il existe, dans le bordereau des prix unitaires (BPU), un prix pour chaque fermeture.

Dans CosWin, la commande d'une visite bimestrielle pour une fermeture fait l'objet d'un ordre de travail (OT) *père*. 
CosWin génère un OT fils par issue et par niche de la fermeture. 
Il en est de même pour les interventions de maintenance annuelle.

Au moment de la commande le PCTT indique sur le bon de commande, dans Sucombe et dans CosWin la date de l'action 
qui est programmée, sur la base du calendrier des fermetures, en concertation avec le titulaire. Dans Sucombe et dans CosWin, cette date définit le délai de réalisation de l'action.

Le titulaire doit extraire de CosWin la table des OTs qui comporte, pour chaque ligne : 

* numéro d'OT (fils),
* tatouage de l'issue ou de la niche,
* délai de réalisation de l'action (date prévue de la visite fixée en fonction des fermetures prévues en concertation avec le titulaire).

Ces données doivent être importées dans l'application de saisie des rapports du titulaire(voir ci-dessous).

## Formats des fichiers à déposer
### Application de saisie des rapports
Le titulaire du marché devra mettre une application de saisie des rapports sur un terminal mobile, à disposition de ses agents intervenant dans les tunnels.
Les rapports seront envoyés directement depuis le terminal de l'agent sur le serveur de la DIRIF.

A ce stade, il est prévu que le serveur soit un **bucket dans Google Storage** sur lequel le titulaire disposera de droit d'écriture.
Ainsi, dans la version de développement, les fichiers peuvent être atteints par une URL du type : 
https://storage.googleapis.com/issues-secours/rapports-visites/345467-3196056.json

### dénomination des rapports
On distingue 4 modèles de rapports :

* rapport de la visite bimestrielle d'une issue (VBIS)
* rapport de la visite bimestrielle d'une niche (VBNI)
* complément de rapport pour la maintenance annuelle d'une issue (MAIS)
* complément de rapport pour la maintenance annuelle d'une niche (MANI)

Le nom du rapport est de la forme : ```<type>-<OT>-<timestamp>.json``` avec :

* type : le code à 4 caractère (VBIS,VBNI,MAIS,MANI)
* OT : le numéro d'OT fils
* le nombre de secondes depuis 01-01-202N mesuré lors de l'enregistrement du rapport, à la fin de l'action dans l'issue ou la niche

Par exemple : `VBIS-345678-26182800` pour une visite terminée le 30-10-2024 à 01h00.

### Points de contrôle
Les rapports sont composés de plusieurs **points de contrôle (PC)**.

Pour chaque point de contrôle, le rapport doit comporter le choix du **résultat du contrôle (RC)** parmi des options prédéfinies et 
un commentaire de l'agent sous la forme d'un texte libre. Le commentaire est obligatoire pour les résultat du contrôle qui traduisent
un défaut majeur ou mineur.

Les listes de **points de contrôle (PC)** et  **résultat du contrôle (RC)** sont :

* [Points de controles des visites bimestrielles des issues](https://raw.githubusercontent.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/refs/heads/master/controleVB_IS.csv)
* https://raw.githubusercontent.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/refs/heads/master/Simulations/controleVB_IS.csv?token=GHSAT0AAAAAACZ2U57VEKWGQGYJ2KU54WGCZZH5FTQ
* Points de controles des visites bimestrielles des niches
* Points de controles complémentaires des interventions de maintenance des issues
* liste

Dans les fichiers les PC et RC sont identifiés par les codes à 3 caractères indiqués dans les listes.

## Contrôle et intégration des fichiers
Les contrôles et les traitements qui seront effectués sur les fichiers déposés par le titulaire sont en cours de rédaction.

On renvoit pour cette étape à ce répertoire :  
[Intégration des données dans BigQuery](https://github.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/tree/master/importeBQ)

Une approche alternative a été explorée ici :  
[Contrôle et production d'un csv](https://github.com/ExploitIdF/TraitementRapportsVisitesBimestrielles/tree/master/logDepot)






