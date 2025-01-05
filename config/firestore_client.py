from google.cloud import firestore
from google.oauth2 import service_account
import os

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if not credentials_path:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")

credentials = service_account.Credentials.from_service_account_file(credentials_path.strip())
db = firestore.Client(credentials=credentials)
