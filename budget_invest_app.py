# budget_invest_app.py
import streamlit as st
from botpress_client import BotpressClient

# 🔐 Load secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

# 🎯 App Layout
st.set_page_config(page_title="🧠 Botpress Chat", layout="centered")
st.title("💬 Ask Your Budgeting Assistant (Botpress)")

user_input = st.text_input("Type your question for the bot:")

if st.button("Submit Botpress Query") and user_input:
    with st.spinner("Contacting Botpress..."):
        try:
            client = BotpressClient(bot_id=BOT_ID, client_id=CLIENT_ID, token=TOKEN)
            convo = client.create_conversation()
            convo_id = convo.get("id")

            if not convo_id:
                st.error("❌ Failed to create conversation with Botpress.")
            else:
                client.send_message(convo_id, user_input)
                reply = client.list_messages(convo_id)

                messages = reply.get("messages", [])
                if messages:
                    last_msg = messages[-1].get("payload", {}).get("text", "⚠️ Bot sent no message.")
                    st.success(f"🤖 Botpress: {last_msg}")
                else:
                    st.warning("⚠️ No messages returned from Botpress.")

        except Exception as e:
            st.error(f"⚠️ Error communicating with Botpress: {e}")
