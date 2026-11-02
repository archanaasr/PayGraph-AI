import requests
from config.settings import get_settings

def get_access_token():
    s=get_settings()
    if not s["paypal_client_id"] or not s["paypal_client_secret"]:
        raise RuntimeError("Set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in .env using PayPal Sandbox credentials.")
    response=requests.post(
        s["paypal_base_url"].rstrip("/")+"/v1/oauth2/token",
        auth=(s["paypal_client_id"],s["paypal_client_secret"]),
        headers={"Accept":"application/json","Accept-Language":"en_US"},
        data={"grant_type":"client_credentials"}, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]
