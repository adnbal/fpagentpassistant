import streamlit as st
from botpress_client import BotpressClient

# Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]

st.set_page_config(page_title="💬 Budget Bot", layout="centered")
st.title("💬 Ask your Budgeting Assistant (Botpress)")

# Initialize session state
if "conversation_id" not in st.session_state:
    try:
        client = BotpressClient(BOT_ID, CLIENT_ID, TOKEN)
        conv = client.create_conversation()
        st.session_state.conversation_id = conv["id"]
        st.session_state.client = client
    except Exception as e:
        st.error("❌ Could not start conversation with Botpress.")
        st.stop()

user_input = st.text_input("Type your message:")
if st.button("Submit") and user_input:
    try:
        client = st.session_state.client
        conversation_id = st.session_state.conversation_id

        client.send_message(conversation_id, user_input)
        st.success("✅ Message sent!")

        st.markdown("**Botpress Reply:**")
        messages = client.get_messages(conversation_id)
        bot_messages = [m for m in messages["messages"] if m["type"] == "text" and m["role"] == "bot"]
        if bot_messages:
            st.write(bot_messages[-1]["payload"]["text"])
        else:
            st.warning("⚠️ No response received from Botpress.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
