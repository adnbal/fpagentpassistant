# botpress_client.py

import requests

class BotpressClient:
    def __init__(self, api_id, token):
        self.api_id = api_id
        self.token = token
        self.api_url = f"https://chat.botpress.cloud/{self.api_id}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Botpress-API-URL": self.api_url
        }

    def create_conversation(self):
        url = f"https://chat.botpress.cloud/api/v1/conversations"
        response = requests.post(url, headers=self.headers)
        if response.status_code != 200:
            print("⚠️ Failed to create conversation:", response.text)
        return response.json()

    def send_message(self, conversation_id, message_text):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        data = {
            "type": "text",
            "payload": {
                "text": message_text
            }
        }
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code != 200:
            print("⚠️ Failed to send message:", response.text)
        return response.json()

    def list_messages(self, conversation_id):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("⚠️ Failed to retrieve messages:", response.text)
        return response.json()
