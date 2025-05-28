import requests
import os
service_url = "https://charger-rapport-222260276716.europe-west1.run.app"
FILE_TO_UPLOAD = "mon_fichier.txt"
def upload_file_to_cloud_run(service_url, file_path):
    """
    Envoie un fichier texte au service Cloud Run via une requête POST.
    """
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier '{file_path}' n'existe pas.")
        return
    upload_endpoint = f"{service_url}/upload"

    try:
        # Ouvrir le fichier en mode binaire pour l'envoi
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/plain')} # ou 'application/octet-stream'

            print(f"Tentative d'envoi de '{file_path}' à '{upload_endpoint}'...")
            response = requests.post(upload_endpoint, files=files)
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)

            print("\n--- Réponse du Serveur ---")
            print(f"Statut HTTP : {response.status_code}")
            print(f"Corps de la réponse : {response.json()}") # Suppose que le serveur renvoie du JSON
            print("--------------------------")

            if response.status_code == 200:
                print(f"Succès : Le fichier '{file_path}' a été uploadé avec succès.")
            else:
                print(f"Échec : Erreur inattendue lors de l'upload.")

    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP lors de l'envoi du fichier : {e}")
        print(f"Réponse du serveur (si disponible) : {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Erreur de connexion : Impossible d'atteindre le serveur. Vérifiez l'URL et votre connexion internet.")
        print(f"Détails : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

if __name__ == "__main__":
    # --- Créer un fichier de test si inexistant ---
    if not os.path.exists(FILE_TO_UPLOAD):
        print(f"Création du fichier de test '{FILE_TO_UPLOAD}'...")
        with open(FILE_TO_UPLOAD, 'w') as f:
            f.write("Ceci est un test d'upload depuis le client Python.\n")
            f.write("Il devrait apparaître dans votre bucket Google Cloud Storage.\n")
        print("Fichier de test créé.")
    upload_file_to_cloud_run(CLOUD_RUN_SERVICE_URL, FILE_TO_UPLOAD)
