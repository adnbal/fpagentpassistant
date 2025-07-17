import gradio as gr
import requests
import os
import pyttsx3

# 🛠️ Botpress Config
BOTPRESS_API_ID = os.getenv("BOTPRESS_API_ID") or "your_botpress_chat_api_id"
BOTPRESS_TOKEN = os.getenv("BOTPRESS_TOKEN") or "your_botpress_token"

class BotpressClient:
    def __init__(self, api_id, token):
        self.api_id = api_id
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-Botpress-API-URL": f"https://chat.botpress.cloud/{api_id}"
        }

    def create_conversation(self):
        url = "https://chat.botpress.cloud/api/v1/conversations"
        response = requests.post(url, headers=self.headers)
        return response.json().get("id")

    def send_message(self, conversation_id, text):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        payload = {"type": "text", "text": text}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.status_code == 200

    def get_latest_reply(self, conversation_id):
        url = f"https://chat.botpress.cloud/api/v1/conversations/{conversation_id}/messages"
        response = requests.get(url, headers=self.headers)
        messages = response.json()
        bot_messages = [m for m in messages if m["type"] == "text" and m["author"]["type"] == "Bot"]
        return bot_messages[-1]["text"] if bot_messages else "No response yet."

# 🔁 Conversation memory
conversation_id = None
bot_client = BotpressClient(BOTPRESS_API_ID, BOTPRESS_TOKEN)

# 🎙️ Voice assistant logic
def voice_assistant(audio):
    global conversation_id
    if not conversation_id:
        conversation_id = bot_client.create_conversation()

    text = audio  # Already converted to text by Gradio
    success = bot_client.send_message(conversation_id, text)
    if not success:
        return "Failed to send message."

    reply = bot_client.get_latest_reply(conversation_id)

    # 🔊 Speak response
    engine = pyttsx3.init()
    engine.say(reply)
    engine.runAndWait()

    return reply

# 🎛️ Gradio UI
gr.Interface(
    fn=voice_assistant,
    inputs=gr.Audio(source="microphone", type="text"),
    outputs="text",
    title="🎙️ Your Personal AI Assistant",
    description="Speak to your Streamlit + Botpress agent"
).launch()
