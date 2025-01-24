from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Define the scopes your application needs, modify as needed
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform', # Modify scopes as needed
]

def run_local_auth():
    """Run local OAuth 2.0 flow to obtain credentials."""
    # Create flow instance using client secrets file
    flow = InstalledAppFlow.from_client_secrets_file(
        'secret.json',  # Your downloaded OAuth 2.0 client secrets file
        scopes=SCOPES
    )

    # Run the flow locally. This will open a browser window for authentication
    credentials = flow.run_local_server(port=8080)

    # Get the token information
    token_info = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    # Save token info to a file
    with open('auth_tokens.json', 'w') as token_file:
        json.dump(token_info, token_file)

    print("Authentication successful!")
    print("Token info saved to auth_tokens.json")
    print(f"Refresh token: {credentials.refresh_token}")
    print("Save this refresh token securely - you'll need it for your application.")


if __name__ == '__main__':
    run_local_auth()
