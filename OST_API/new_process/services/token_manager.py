# token_manager.py
import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from config import PROXY, USE_PROXY

class token_manager:
    def __init__(self, api_url, client_id, client_secret, refresh_interval=1800):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.proxy = PROXY if USE_PROXY else None
        self.token = None
        self.token_lock = threading.Lock()
        self.scheduler = BackgroundScheduler()
        self.refresh_interval = refresh_interval

        self.scheduler.start()
        self.fetch_token()
        self.scheduler.add_job(self.fetch_token, 'interval', seconds=self.refresh_interval)

    def fetch_token(self):
        response = requests.post(self.api_url, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }, proxies=self.proxy)

        if response.status_code == 200:
            token_data = response.json()
            with self.token_lock:
                self.token = token_data['access_token']
            print("Token refreshed successfully")
        else:
            print("Failed to fetch token:", response.status_code, response.text)

    def get_token(self):
        with self.token_lock:
            return self.token

    def stop(self):
        self.scheduler.shutdown()
