import streamlit as st
from botpress_client import BotpressClient

# 🔐 Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

# 📄 Streamlit Config
st.set_page_config(page_title="💬 Budgeting Chat Assistant", layout="wide")
st.title("💬 Budgeting Chat Assistant")

# 📥 User input
user_input = st.text_input("Type your question for the bot:")

# 📤 Submit to Botpress
if st.button("Submit Botpress Query") and user_input:
    try:
        client = BotpressClient(bot_id=BOT_ID, client_id=CLIENT_ID, token=TOKEN)
        convo = client.create_conversation()
        convo_id = convo.get("id")

        if convo_id:
            client.send_message(convo_id, user_input)
            messages = client.list_messages(convo_id)
            if messages:
                last_msg = messages[-1].get("payload", {}).get("text", "⚠️ No response received.")
                st.success(f"🤖 Bot: {last_msg}")
            else:
                st.warning("⚠️ No messages returned from Botpress.")
        else:
            st.error("❌ Failed to create conversation.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
