from google.cloud import secretmanager
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def get_secret(project_id, secret_name, version="latest"):
    """Retrieve secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def create_cm360_client(project_id):
    """Create an authenticated CM360 client using service account credentials."""
    # Get service account key from Secret Manager
    sa_key_json = get_secret(project_id, "cm360-sa-key")
    sa_key_dict = json.loads(sa_key_json)
    
    # Define required scopes
    SCOPES = [
        'https://www.googleapis.com/auth/dfareporting',
        'https://www.googleapis.com/auth/dfatrafficking'
    ]
    
    # Create credentials from service account key
    credentials = service_account.Credentials.from_service_account_info(
        sa_key_dict,
        scopes=SCOPES
    )
    
    # Create the CM360 service
    service = build('dfareporting', 'v4', credentials=credentials)
    return service

def example_usage(project_id):
    """Example of using the CM360 client."""
    try:
        service = create_cm360_client(project_id)
        
        # Example: List user profiles
        profiles = service.userProfiles().list().execute()
        
        return {
            'status': 'success',
            'profiles': profiles.get('items', [])
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
