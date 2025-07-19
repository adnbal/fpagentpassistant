import requests
import time

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.base_url = f"https://chat.botpress.cloud/v1"

    def create_conversation(self):
        url = f"{self.base_url}/conversations"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-bot-id": self.bot_id,
            "x-client-id": self.client_id,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            return None, response.text
        return response.json().get("id"), None

    def send_message(self, convo_id, message):
        url = f"{self.base_url}/conversations/{convo_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-bot-id": self.bot_id,
            "x-client-id": self.client_id,
            "Content-Type": "application/json"
        }
        payload = {
            "type": "text",
            "text": message
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code, response.text

    def get_messages(self, convo_id):
        url = f"{self.base_url}/conversations/{convo_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-bot-id": self.bot_id,
            "x-client-id": self.client_id
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, response.text
        return response.json().get("messages", []), None
