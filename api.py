import requests
import hashlib
import base64
import json
from auth import get_token
import os

BASE_URL = os.getenv("API_BASE_URL")

def _auth_headers():
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json"
    }

def validate_tin(tin, id_type, id_value):
    url = f"{BASE_URL}/api/v1.0/taxpayer/validate/{tin}?idType={id_type}&idValue={id_value}"
    return requests.get(url, headers=_auth_headers()).json()

def submit_document(data, format="JSON"):
    document_str = json.dumps(data, separators=(',', ':'))
    encoded_doc = base64.b64encode(document_str.encode()).decode()
    hash_val = hashlib.sha256(document_str.encode()).hexdigest()

    payload = {
        "documents": [{
            "format": format,
            "document": encoded_doc,
            "documentHash": hash_val,
            "codeNumber": data.get("invoice_number", "Unknown")
        }]
    }

    url = f"{BASE_URL}/api/v1.0/documentsubmissions/"
    return requests.post(url, json=payload, headers=_auth_headers()).json()

def cancel_document(uuid, reason):
    url = f"{BASE_URL}/api/v1.0/documents/state/{uuid}/state"
    return requests.put(url, json={"status": "cancelled", "reason": reason}, headers=_auth_headers()).json()

def reject_document(uuid, reason):
    url = f"{BASE_URL}/api/v1.0/documents/state/{uuid}/state"
    return requests.put(url, json={"status": "rejected", "reason": reason}, headers=_auth_headers()).json()

