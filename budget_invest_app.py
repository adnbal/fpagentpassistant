import streamlit as st
import requests

# ✅ Streamlit page config
st.set_page_config(page_title="💬 Budget Assistant with Botpress", layout="centered")
st.title("💬 Budgeting Assistant (Botpress AI)")

# ✅ Botpress credentials from secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

# ✅ Botpress Client
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

# ✅ UI Input
user_input = st.text_input("Type your question for the bot:")

# ✅ Button: Submit
if st.button("Submit Botpress Query") and user_input:
    client = BotpressClient(bot_id=BOT_ID, client_id=CLIENT_ID, token=TOKEN)
    
    try:
        convo = client.create_conversation()
        convo_id = convo.get("id")

        if convo_id:
            client.send_message(convo_id, user_input)
            messages = client.list_messages(convo_id)

            if "messages" in messages and messages["messages"]:
                # Show last message from bot
                last_message = messages["messages"][-1]
                if last_message["type"] == "text":
                    st.success(f"🤖 Bot: {last_message['payload']['text']}")
                else:
                    st.warning("⚠️ Bot returned non-text message.")
            else:
                st.warning("⚠️ No messages returned from Botpress.")
        else:
            st.error("❌ Failed to create conversation.")
    
    except Exception as e:
        st.error(f"❌ Error communicating with Botpress: {e}")
