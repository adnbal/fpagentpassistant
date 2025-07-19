import streamlit as st
import requests
import google.generativeai as genai

# 🔐 Load Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]
GEMINI_KEY = st.secrets["gemini"]["api_key"]
DEEPSEEK_KEY = st.secrets["openrouter"]["api_key"]

# 🔧 Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# 📄 App Config
st.set_page_config(page_title="💬 Budgeting Chat Assistant", layout="centered")
st.title("💬 Budgeting Chat Assistant")

# ✨ Input UI
user_input = st.text_input("Type your question for the bot:")
submit = st.button("Submit")

# 💬 Botpress API URLs
CONVO_URL = f"https://chat.botpress.cloud/v1/conversations"
MESSAGE_URL = lambda cid: f"https://chat.botpress.cloud/v1/conversations/{cid}/messages"

# 📤 Talk to Botpress
def talk_to_botpress(question):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-Bot-Id": BOT_ID,
        "X-Client-Id": CLIENT_ID,
        "Content-Type": "application/json"
    }

    # 🗨️ Step 1: Create conversation
    convo_res = requests.post(CONVO_URL, headers=headers)
    if convo_res.status_code != 200:
        return f"❌ Failed to start conversation: {convo_res.text}"

    convo_id = convo_res.json().get("id")
    if not convo_id:
        return "❌ Could not retrieve conversation ID."

    # 📩 Step 2: Send user message
    message_payload = {
        "type": "text",
        "text": question
    }
    send_res = requests.post(MESSAGE_URL(convo_id), headers=headers, json=message_payload)
    if send_res.status_code != 200:
        return f"❌ Failed to send message: {send_res.text}"

    # 🕒 Wait for reply
    import time
    time.sleep(2)

    # 📥 Step 3: Get bot reply
    get_res = requests.get(MESSAGE_URL(convo_id), headers=headers)
    if get_res.status_code != 200:
        return f"⚠️ No messages returned from Botpress."

    messages = get_res.json().get("messages", [])
    bot_reply = next((m["payload"]["text"] for m in messages[::-1] if m.get("type") == "text" and m.get("role") == "bot"), None)

    return bot_reply or "⚠️ No response received from Botpress."

# 🚀 Trigger on Submit
if submit and user_input:
    with st.spinner("Talking to your budgeting assistant..."):
        response = talk_to_botpress(user_input)
        st.markdown(f"**Bot Response:** {response}")
