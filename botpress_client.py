import requests

class BotpressClient:
    def __init__(self, api_id, user_key):
        self.bot_id = api_id
        self.token = user_key
        self.base_url = "https://chat.botpress.cloud/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_conversation(self):
        url = f"{self.base_url}/conversations"
        payload = {
            "botId": self.bot_id
        }
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
        return response.json()

    def list_messages(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print("❌ Failed to retrieve messages:", response.text)
        return response.json()
