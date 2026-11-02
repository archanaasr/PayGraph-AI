"""Webhook verification helper. Configure a webhook ID in PayPal and verify events before trusting them."""
import requests
from .authentication import get_access_token
from config.settings import get_settings

def verify_webhook(headers, event, webhook_id):
    token=get_access_token(); s=get_settings()
    payload={"auth_algo":headers.get("PAYPAL-AUTH-ALGO"),
      "cert_url":headers.get("PAYPAL-CERT-URL"),
      "transmission_id":headers.get("PAYPAL-TRANSMISSION-ID"),
      "transmission_sig":headers.get("PAYPAL-TRANSMISSION-SIG"),
      "transmission_time":headers.get("PAYPAL-TRANSMISSION-TIME"),
      "webhook_id":webhook_id,"webhook_event":event}
    r=requests.post(s["paypal_base_url"].rstrip("/")+"/v1/notifications/verify-webhook-signature",
      headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json=payload,timeout=30)
    r.raise_for_status()
    return r.json().get("verification_status")=="SUCCESS"
