import requests

class BotpressClient:
    def __init__(self, bot_id, client_id, token):
        self.bot_id = bot_id
        self.client_id = client_id
        self.token = token
        self.base_url = "https://chat.botpress.cloud"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_conversation(self):
        url = f"{self.base_url}/api/v1/bots/{self.bot_id}/conversations"
        payload = {"clientId": self.client_id}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def send_message(self, conversation_id, message):
        url = f"{self.base_url}/api/v1/bots/{self.bot_id}/conversations/{conversation_id}/messages"
        payload = {
            "type": "text",
            "text": message,
            "role": "user"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_messages(self, conversation_id):
        url = f"{self.base_url}/api/v1/bots/{self.bot_id}/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
