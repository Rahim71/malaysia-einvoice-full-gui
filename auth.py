import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_token():
    """Get JWT access token from LHDN Identity Service."""
    url = os.getenv("TOKEN_URL")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    onbehalfof = os.getenv("ON_BEHALF_OF")

    if not all([url, client_id, client_secret]):
        raise EnvironmentError("Missing required environment variables (TOKEN_URL, CLIENT_ID, CLIENT_SECRET)")

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'InvoicingAPI'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    if onbehalfof:
        headers['onbehalfof'] = onbehalfof

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        error_msg = f"Token request failed: {response.status_code} - {response.text}"
        raise Exception(error_msg)
