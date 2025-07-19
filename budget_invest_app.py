import requests

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Bot-Id": self.bot_id,
            "X-Client-Id": self.client_id,
            "Content-Type": "application/json"
        }

    def create_conversation(self):
        url = f"https://chat.botpress.cloud/api/v1/conversations"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def send_message(self, conversation_id, text):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        data = {
            "type": "text",
            "payload": {
                "text": text
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def list_messages(self, conversation_id):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        return response.json()
