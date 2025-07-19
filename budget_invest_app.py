import streamlit as st
from botpress_client import BotpressClient

# 🔐 Load secrets from Streamlit Cloud
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

# 🎯 UI
st.set_page_config(page_title="💬 Budgeting Chat Assistant", layout="centered")
st.title("💬 Budgeting Chat Assistant")
user_input = st.text_input("Type your question for the bot:")

if st.button("Submit Botpress Query") and user_input:
    try:
        client = BotpressClient(bot_id=BOT_ID, client_id=CLIENT_ID, token=TOKEN)
        
        # 🧪 Debug: Creating conversation
        convo = client.create_conversation()
        st.write("✅ Conversation created:", convo)

        convo_id = convo.get("id")
        if convo_id:
            # 🧪 Debug: Sending message
            client.send_message(convo_id, user_input)

            # 🧪 Debug: Getting response
            messages = client.list_messages(convo_id)
            st.write("📩 All messages:", messages)

            if messages:
                last_msg = messages[-1].get("payload", {}).get("text", "⚠️ No response received.")
                st.success(f"🤖 Bot: {last_msg}")
            else:
                st.warning("⚠️ No messages returned from Botpress.")
        else:
            st.error("❌ Failed to get conversation ID.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
