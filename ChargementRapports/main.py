import os
from flask import Flask, request, jsonify
from google.cloud import storage
import logging

# Configurez le logging pour voir les messages dans les logs Cloud Run
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
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
    bucket_name = 'rapports-batiment'
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
