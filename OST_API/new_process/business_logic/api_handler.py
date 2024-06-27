# api_handler.py
from services.token_manager import token_manager
from config import PROXY, USE_PROXY

def call_api(endpoint, data):
    token = token_manager.get_token()
    proxies = PROXY if USE_PROXY else None
    response = requests.post(endpoint, headers={"Authorization": f"Bearer {token}"}, json=data, proxies=proxies)
    return response.json()
