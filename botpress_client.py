import requests

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.base_url = "https://chat.botpress.cloud/api/v1"

    def create_conversation(self):
        url = f"{self.base_url}/conversations"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Bot-Id": self.bot_id,
            "X-Client-Id": self.client_id
        }
        response = requests.post(url, headers=headers)
        return response.json()

    def send_message(self, conversation_id, message):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Bot-Id": self.bot_id,
            "X-Client-Id": self.client_id,
            "Content-Type": "application/json"
        }
        data = {
            "type": "text",
            "payload": {
                "text": message
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def list_messages(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Bot-Id": self.bot_id,
            "X-Client-Id": self.client_id
        }
        response = requests.get(url, headers=headers)
        return response.json()
