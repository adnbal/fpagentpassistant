# botpress_client.py

import requests

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.api_url = f"https://chat.botpress.cloud/api/v1"

    def create_conversation(self):
        url = f"{self.api_url}/conversations"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-bot-id": self.bot_id,
            "x-client-id": self.client_id
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()["id"]

    def send_message(self, conversation_id, message):
        url = f"{self.api_url}/conversations/{conversation_id}/messages"
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
        response.raise_for_status()
        return response.json()

    def list_messages(self, conversation_id):
        url = f"{self.api_url}/conversations/{conversation_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "x-bot-id": self.bot_id,
            "x-client-id": self.client_id
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
