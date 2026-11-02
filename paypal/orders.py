import requests
from .authentication import get_access_token
from config.settings import get_settings

def create_order(amount, currency="USD"):
    token=get_access_token()
    s=get_settings()
    payload={"intent":"CAPTURE","purchase_units":[{"amount":{"currency_code":currency,"value":f"{float(amount):.2f}"}}]}
    response=requests.post(s["paypal_base_url"].rstrip("/")+"/v2/checkout/orders",
        headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},
        json=payload,timeout=30)
    response.raise_for_status()
    return response.json()

def capture_order(order_id):
    token=get_access_token()
    s=get_settings()
    response=requests.post(s["paypal_base_url"].rstrip("/")+f"/v2/checkout/orders/{order_id}/capture",
        headers={"Authorization":f"Bearer {token}","Content-Type":"application/json"},json={},timeout=30)
    response.raise_for_status()
    return response.json()
