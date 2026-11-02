import os
from dotenv import load_dotenv
load_dotenv()

def get_settings():
    return {
        "paypal_client_id": os.getenv("PAYPAL_CLIENT_ID",""),
        "paypal_client_secret": os.getenv("PAYPAL_CLIENT_SECRET",""),
        "paypal_base_url": os.getenv("PAYPAL_BASE_URL","https://api-m.sandbox.paypal.com"),
        "openai_api_key": os.getenv("OPENAI_API_KEY",""),
        "openai_model": os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        "database_url": os.getenv("DATABASE_URL","sqlite:///paygraph.db"),
    }
