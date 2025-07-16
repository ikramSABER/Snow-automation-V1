import requests
from requests.auth import HTTPBasicAuth

class JiraUpload:
    def upload_file(self, ticket_key, file_path, email, api_token):
        url = f"https://riadamine59.atlassian.net/rest/api/2/issue/{ticket_key}/attachments"
        headers = {
            "X-Atlassian-Token": "no-check"
        }
        auth = HTTPBasicAuth(email, api_token)
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/octet-stream')}
            response = requests.post(url, headers=headers, files=files, auth=auth)

        if response.status_code == 200:
            print("✅ Pièce jointe ajoutée avec succès !")
            return "SUCCESS"
        else:
            print(f"❌ Échec avec statut : {response.status_code}, Réponse : {response.text}")
            raise Exception(f"Erreur upload : {response.status_code} {response.text}")
