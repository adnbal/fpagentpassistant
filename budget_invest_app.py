import streamlit as st
from botpress_client import BotpressClient
import time

# Load secrets
BOT_ID = st.secrets["botpress"]["bot_id"]  # from your webchat embed
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

bot_client = BotpressClient(BOT_ID, CLIENT_ID, TOKEN)

st.title("💬 Budgeting Chat Assistant")
user_input = st.text_input("Type your question for the bot:")

if st.button("Submit") and user_input:
    st.write("🛠️ Creating conversation...")
    convo_id, error = bot_client.create_conversation()
    if error:
        st.error(f"❌ Failed to create conversation: {error}")
    else:
        st.write("✉️ Sending message...")
        status_code, response_text = bot_client.send_message(convo_id, user_input)
        if status_code != 200:
            st.error(f"❌ Failed to send message: {response_text}")
        else:
            st.write("⏳ Waiting for bot response...")
            time.sleep(5)  # Wait for bot to respond

            messages, err = bot_client.get_messages(convo_id)
            if err:
                st.error(f"⚠️ No messages returned from Botpress. {err}")
            else:
                st.write("📨 All messages:", messages)  # Debug log
                bot_reply = next((m["payload"]["text"] for m in reversed(messages)
                                  if m.get("type") == "text" and m.get("role") == "bot"), None)
                if bot_reply:
                    st.success(f"🤖 Bot Response: {bot_reply}")
                else:
                    st.warning("⚠️ Bot did not send a text response.")
