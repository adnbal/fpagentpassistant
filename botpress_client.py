import requests

class BotpressClient:
    def __init__(self, api_id, user_key):
        self.api_id = api_id
        self.user_key = user_key
        self.headers = {
            "Authorization": f"Bearer {self.user_key}",
            "X-Botpress-API-URL": f"https://chat.botpress.cloud/{self.api_id}"
        }

    def create_conversation(self):
        url = "https://chat.botpress.cloud/api/v1/conversations"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def list_messages(self, conversation_id):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def send_message(self, conversation_id, message):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        payload = {"type": "text", "text": message}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()
