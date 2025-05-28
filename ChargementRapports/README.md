# Chargement des rapports
Absolument ! Nous allons créer un petit programme Python qui agit comme un serveur web simple (avec Flask) pour recevoir un fichier texte via une requête HTTP POST et l'enregistrer dans un bucket Google Cloud Storage (GCS). Ensuite, je vous expliquerai comment le déployer sur Cloud Run.

---

### **Partie 1 : Le Programme Python (Serveur Flask)**

Ce programme Python utilisera la bibliothèque `google-cloud-storage` pour interagir avec GCS, mais le client qui enverra le fichier n'aura pas besoin de cette bibliothèque ; il utilisera simplement HTTP.

**1. Structure du Projet :**

Créez un dossier pour votre projet, par exemple `my-gcs-uploader`. À l'intérieur de ce dossier, créez les fichiers suivants :

```
my-gcs-uploader/
├── main.py
├── requirements.txt
└── .gcloudignore (optionnel, mais recommandé)
```

**2. `requirements.txt` :**

Ce fichier liste les dépendances Python de votre projet.

```
Flask
google-cloud-storage
```

**3. `main.py` :**

C'est le code de votre serveur web.

```python
import os
from flask import Flask, request, jsonify
from google.cloud import storage
import logging

# Configurez le logging pour voir les messages dans les logs Cloud Run
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Assurez-vous que la variable d'environnement GOOGLE_CLOUD_PROJECT est définie
# ou passez l'ID de votre projet directement au client Storage
# Pour Cloud Run, le client Storage va généralement déduire le projet de l'environnement
# et s'authentifier via le compte de service du service Cloud Run.
# Assurez-vous que le compte de service de Cloud Run a les droits d'écriture sur GCS.
storage_client = storage.Client() # Le projectId sera déduit

@app.route('/', methods=['GET'])
def index():
    """Page d'accueil simple pour vérifier que le service est en ligne."""
    logger.info("Requête GET reçue sur la racine.")
    return "Bonjour de l'uploader Cloud Run ! Envoyez un fichier texte via POST à /upload."

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint pour uploader un fichier texte vers Google Cloud Storage.
    Le nom du fichier est attendu dans le champ 'filename' du formulaire FormData,
    et le contenu du fichier dans le champ 'file'.
    """
    logger.info("Requête POST reçue sur /upload.")

    if 'file' not in request.files:
        logger.warning("Aucun fichier trouvé dans la requête.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning("Aucun fichier sélectionné.")
        return jsonify({"error": "No selected file"}), 400

    # Récupérer le nom du bucket depuis une variable d'environnement Cloud Run
    # C'est une bonne pratique pour ne pas hardcoder le nom du bucket dans le code.
    bucket_name = os.getenv('GCS_BUCKET_NAME')
    if not bucket_name:
        logger.error("La variable d'environnement GCS_BUCKET_NAME n'est pas définie.")
        return jsonify({"error": "GCS_BUCKET_NAME environment variable not set."}), 500

    # Utiliser le nom de fichier original ou en générer un unique
    destination_blob_name = file.filename
    if not destination_blob_name:
        # Fallback si le nom de fichier est vide, générer un nom unique
        import uuid
        destination_blob_name = f"uploaded_file_{uuid.uuid4().hex}.txt"
        logger.info(f"Nom de fichier vide, généré: {destination_blob_name}")
    else:
        logger.info(f"Fichier reçu: {destination_blob_name}")


    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Lire le contenu du fichier directement depuis le stream
        file_content = file.read()
        
        # Uploader le contenu
        blob.upload_from_string(file_content, content_type=file.content_type)

        logger.info(f"Fichier {destination_blob_name} uploadé vers le bucket {bucket_name}.")
        return jsonify({
            "message": f"File {destination_blob_name} uploaded successfully to {bucket_name}.",
            "public_url": blob.public_url # Si le bucket est public ou si vous voulez l'URL de l'objet
        }), 200

    except Exception as e:
        logger.exception(f"Erreur lors de l'upload du fichier {destination_blob_name}: {e}")
        return jsonify({"error": f"Failed to upload file: {str(e)}"}), 500

if __name__ == '__main__':
    # Cloud Run injecte la variable d'environnement PORT
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Démarrage du serveur sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) # debug=True seulement en développement local
```

**Explication du `main.py` :**

* **`storage.Client()`**: Initialise le client GCS. Sur Cloud Run, il s'authentifie automatiquement via le compte de service du service Cloud Run et détecte le projet ID.
* **`@app.route('/upload', methods=['POST'])`**: Définit une route `/upload` qui accepte uniquement les requêtes POST.
* **`request.files['file']`**: Accède au fichier envoyé dans le corps de la requête HTTP via un formulaire `multipart/form-data`. Le nom du champ attendu est `file`.
* **`os.getenv('GCS_BUCKET_NAME')`**: Récupère le nom du bucket depuis une variable d'environnement. **C'est crucial pour la flexibilité du déploiement.**
* **`blob.upload_from_string(file_content, content_type=file.content_type)`**: Uploade le contenu binaire du fichier vers GCS. `content_type` est important pour que GCS serve correctement le fichier.
* **`app.run(host='0.0.0.0', port=port)`**: Démarre le serveur Flask. Cloud Run injecte le port d'écoute via la variable d'environnement `PORT`.

**4. `.gcloudignore` (Optionnel mais Recommandé) :**

Ce fichier indique à Cloud Build (utilisé par Cloud Run pour construire votre image) les fichiers et dossiers à ignorer lors de la création de l'image Docker. Cela réduit la taille de l'image et accélère la construction.

```
.gcloudignore
.git
.gitignore
.env
__pycache__/
*.pyc
venv/
node_modules/
```

---

### **Partie 2 : Déploiement sur Google Cloud Run**

Pour déployer ce programme sur Cloud Run, vous utiliserez Cloud Build pour transformer votre code source en une image conteneur, puis déployer cette image.

**Pré-requis :**

1.  **Un projet Google Cloud actif (`sucombe` dans votre cas).**
2.  **Un bucket Google Cloud Storage.** Créez-en un si vous n'en avez pas : `gsutil mb gs://votre-nom-de-bucket-uploader-unique` (les noms de bucket doivent être globalement uniques).
3.  **Permissions IAM :**
    * Votre compte utilisateur doit avoir des rôles comme `Cloud Run Admin` et `Cloud Build Editor` pour déployer.
    * Le **compte de service par défaut de Cloud Run** (généralement `PROJECT_NUMBER-compute@developer.gserviceaccount.com`) aura besoin du rôle `Storage Object Admin` ou `Storage Object Creator` sur le bucket que vous utiliserez, pour pouvoir y écrire des fichiers.
    * Le **compte de service Cloud Build** (généralement `PROJECT_NUMBER@cloudbuild.gserviceaccount.com`) aura besoin des permissions pour stocker des images dans Container Registry (souvent incluses par défaut).

**Étapes de Déploiement :**

1.  **Poussez votre code vers un dépôt Git (GitHub, GitLab, Cloud Source Repositories) :**
    ```bash
    cd my-gcs-uploader
    git init
    git add .
    git commit -m "Initial commit for GCS uploader"
    # Configurez un dépôt distant (par exemple, sur GitHub) et poussez votre code.
    git remote add origin https://github.com/votre_utilisateur/my-gcs-uploader.git
    git push -u origin main
    ```

2.  **Déployer via la Console GCP :**

    * Allez dans la console Google Cloud, sélectionnez votre projet (`sucombe`).
    * Naviguez vers **Cloud Run**.
    * Cliquez sur **"CREATE SERVICE"** (ou "DEPLOY NEW REVISION" si c'est un service existant).

    * **Configuration de base :**
        * **Service name:** `gcs-file-uploader` (ou le nom que vous voulez)
        * **Region:** Choisissez une région proche de vos utilisateurs ou de votre bucket (ex: `europe-west1`).

    * **Source repository :**
        * Sélectionnez **"Continuously deploy from a source repository"**.
        * Cliquez sur **"SETUP CONTINUOUS DEPLOYMENT"**.
        * Connectez votre fournisseur Git (GitHub, GitLab, Bitbucket) ou utilisez Cloud Source Repositories.
        * Sélectionnez le dépôt (`my-gcs-uploader`).
        * Sélectionnez la branche (`main`).
        * **Build context directory:** Laissez vide (ou mettez `.`) si `main.py` est à la racine de votre dépôt. Si votre code est dans un sous-dossier (ex: `src`), mettez `src/`.

    * **Build Configuration / Runtime :**
        * Le système de Buildpacks devrait détecter automatiquement que c'est une application Python.
        * **Entrypoint:** **Laissez vide.** Le Buildpack Python détectera Flask et le lancera.
        * **Function target:** **Laissez vide.** Ce n'est pas une fonction Cloud Function style, mais un serveur web complet.

    * **Environment variables:**
        * C'est ici que vous allez définir le nom de votre bucket !
        * Cliquez sur **"ADD VARIABLE"**.
        * **Name:** `GCS_BUCKET_NAME`
        * **Value:** `votre-nom-de-bucket-uploader-unique` (remplacez par le nom de votre bucket GCS)

    * **Authentication :**
        * Choisissez **"Allow unauthenticated invocations"** si vous voulez que n'importe qui puisse uploader (pour un test simple). **Pour la production, il est fortement recommandé d'utiliser "Require authentication" et de sécuriser votre endpoint.**

    * **Cliquez sur "DEPLOY".**

    Cloud Build va alors s'activer pour construire votre image conteneur et Cloud Run va la déployer. Cela peut prendre quelques minutes.

---

### **Partie 3 : Comment Uploader un Fichier (Test)**

Une fois votre service Cloud Run déployé et son URL disponible, vous pouvez tester l'upload.

1.  **Récupérez l'URL de votre service Cloud Run.** Elle sera affichée dans la console Cloud Run une fois le déploiement réussi.

2.  **Utilisez `curl` pour tester :**
    Créez un petit fichier texte localement, par exemple `mon_test.txt` avec le contenu `Ceci est un fichier de test.`

    ```bash
    # Remplacez <CLOUD_RUN_URL> par l'URL de votre service Cloud Run
    # Remplacez mon_test.txt par le chemin de votre fichier local
    curl -X POST -F "file=@/chemin/vers/mon_test.txt" <CLOUD_RUN_URL>/upload
    ```

    * `-X POST`: Indique que c'est une requête POST.
    * `-F "file=@/chemin/vers/mon_test.txt"`: Envoie le fichier `/chemin/vers/mon_test.txt` dans le champ `file` du formulaire `multipart/form-data`. Le `@` est crucial pour indiquer à `curl` que c'est un fichier.

    Vous devriez recevoir une réponse JSON de votre service Cloud Run indiquant le succès de l'upload.

3.  **Vérifiez dans le bucket GCS :**
    Allez dans la console Google Cloud, naviguez vers **Cloud Storage** > **Buckets**, puis sélectionnez votre bucket. Vous devriez y voir votre fichier `mon_test.txt` (ou le nom généré si le nom était vide).

Ce setup vous permet d'uploader des fichiers vers GCS via une simple requête HTTP POST, sans que le client n'ait à gérer l'authentification Google Cloud ou les bibliothèques spécifiques à GCS.


