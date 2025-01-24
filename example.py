from google.cloud import secretmanager
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

def get_secret(project_id, secret_name, version="latest"):
    """
      Retrieve secret from Secret Manager. This can be replaced with simply
      fetching the auth_token.json file that was generated in the initial auth
      step, but it is generally recommended that these credentials are stored
      remotely + securely and not locally.
    """
    
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def create_cm360_client(project_id):
    """
      Create an authenticated CM360 client using stored credentials.
    """
    # Get stored credentials from Secret Manager
    auth_tokens = json.loads(get_secret(project_id, "auth_tokens"))
    
    # Create credentials object
    credentials = Credentials(
        token=None,  # We'll use refresh token, so no need for access token
        refresh_token=auth_tokens['refresh_token'],
        token_uri=auth_tokens['token_uri'],
        client_id=auth_tokens['client_id'],
        client_secret=auth_tokens['client_secret'],
        scopes=auth_tokens['scopes']
    )

    # Create the CM360 service
    service = build(
      'dfareporting', 
      'v4', 
      credentials=credentials
    )
    return service

def example_usage(project_id):
    """Example of using the CM360 client."""
    try:
        service = create_cm360_client(project_id)
        
        # Example: List user profiles
        profiles = service.userProfiles().list().execute()
        
        # Example: List reports for a profile
        profile_id = profiles['items'][0]['profileId']  # Use first available profile
        reports = service.reports().list(profileId=profile_id).execute()
        
        return {
            'status': 'success',
            'reports': reports.get('items', [])
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == "__main__":
  example_usage('YOUR-GCP-PROJECT-ID')
