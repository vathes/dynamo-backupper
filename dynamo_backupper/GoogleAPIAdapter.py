import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account_file.json'

class GoogleAPIAdapter:
    def __init__(self):
        # Load service account info from enviorment variables
        service_account_dict = dict(
            type=os.environ['TYPE'],
            project_id=os.environ['PROJECT_ID'],
            private_key_id=os.environ['PRIVATE_KEY_ID'],
            private_key=os.environ['PRIVATE_KEY'],
            client_email=os.environ['CLIENT_EMAIL'],
            client_id=os.environ['CLIENT_ID'],
            auth_uri=os.environ['AUTH_URI'],
            token_uri=os.environ['TOKEN_URI'],
            auth_provider_x509_cert_url=os.environ['AUTH_PROVIDER_x509_CERT_URL'],
            client_x509_cert_url=os.environ['AUTH_PROVIDER_x509_CERT_URL']
            )

        # Write file to temp storage
        service_account_file = open(SERVICE_ACCOUNT_FILE, 'w')
        service_account_file.write(json.dumps(service_account_dict))
        service_account_file.close()

        self.credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.google_drive_api = build('drive', 'v3', credentials=self.credentials)

    def find_folder_id(self, folder_name):
        # Query files
        files = self.google_drive_api.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

        folder_id = folder_name
        for file in files['files']:
            if file['name'] == folder_name:
                return file['id']

        # Raise exception if folder was not found        
        raise Exception('Could not find' + folder_name)

    def upload_csv_under_folder(self, csv_upload_name, csv_filename_on_disk, folder_id):
        file_metadata = dict(name=csv_upload_name, parents=[folder_id])
        media_body = MediaFileUpload(csv_filename_on_disk, mimetype='text/csv')
        self.google_drive_api.files().create(body=file_metadata, media_body=media_body).execute()