# botpress_client.py

import requests

class BotpressClient:
    def __init__(self, api_id, user_key):
        self.api_id = api_id.replace("bot_", "")  # remove 'bot_' if present
        self.user_key = user_key
        self.headers = {
            "Authorization": f"Bearer {self.user_key}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://chat.botpress.cloud/api/v1"

    def create_conversation(self):
        url = f"{self.base_url}/conversations"
        payload = {"botId": self.api_id}
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print("❌ Failed to create conversation:", response.text)
        return response.json()

    def send_message(self, conversation_id, text):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        payload = {
            "type": "text",
            "text": text
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print("❌ Failed to send message:", response.text)

    def list_messages(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("❌ Failed to fetch messages:", response.text)
        return response.json()
