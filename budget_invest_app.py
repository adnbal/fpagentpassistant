import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai

# 🔐 Secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
TOKEN = st.secrets["botpress"]["token"]

# ✅ Botpress Details
BOT_ID = "16e43556-ccfc-4fea-b39b-a9eefac04ef3"
CLIENT_ID = "94c88ab7-520e-4704-8423-be1670714153"

# ✅ Updated BotpressClient (import this from your botpress_client.py if separated)
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

# ✅ Initialize Botpress client
client = BotpressClient(bot_id=BOT_ID, client_id=CLIENT_ID, token=TOKEN)
