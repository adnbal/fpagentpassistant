# botpress_client.py
import requests

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://chat.botpress.cloud/api/v1"

    def create_conversation(self):
        url = f"{self.base_url}/conversations"
        payload = {
            "botId": self.bot_id,
            "clientId": self.client_id
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def send_message(self, conversation_id, text):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        payload = {
            "type": "text",
            "text": text
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def list_messages(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        return response.json()
