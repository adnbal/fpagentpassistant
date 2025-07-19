import streamlit as st
from botpress_client import BotpressClient

# 🔐 Secrets from .streamlit/secrets.toml
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

# 🎯 Title
st.set_page_config(page_title="🔁 Botpress Minimal Test")
st.title("💬 Ask Botpress Assistant")

# 🚀 Initialize client
if "conversation_id" not in st.session_state:
    client = BotpressClient(BOT_ID, CLIENT_ID, TOKEN)
    convo = client.create_conversation()
    st.session_state.client = client
    st.session_state.conversation_id = convo["id"]

# 📝 Input box
user_input = st.text_input("Type your question for the bot:")

if st.button("Submit"):
    if user_input:
        try:
            client = st.session_state.client
            client.send_message(st.session_state.conversation_id, user_input)
            messages = client.get_messages(st.session_state.conversation_id)
            bot_replies = [
                msg["payload"]["text"]
                for msg in messages["messages"]
                if msg["type"] == "text" and msg["role"] == "bot"
            ]
            if bot_replies:
                st.success("Botpress replied:")
                st.write(bot_replies[-1])
            else:
                st.warning("⚠️ No response received from Botpress.")
        except Exception as e:
            st.error(f"Error: {e}")
