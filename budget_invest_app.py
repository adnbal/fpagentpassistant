import streamlit as st
import requests

# 🔐 Load Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]         # Used only for iframe display
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]
DEEPSEEK_KEY = st.secrets["openrouter"]["api_key"]

# 📄 App Config
st.set_page_config(page_title="💸 Budget & Investment Chat Assistant", layout="centered")
st.title("💬 Budgeting Chat Assistant")

st.markdown("""
Welcome to your **AI-Powered Financial Assistant**!  
Ask anything about your income, expenses, savings, or investments.  
This chat is powered by **DeepSeek AI** for smart, reliable advice.
""")

# 🧠 DeepSeek LLM Response
def get_deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a financial assistant. Provide clear, useful budgeting and investment advice."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        return f"⚠️ Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# 💬 User Input
query = st.text_input("💬 Ask something about budgeting or investing:")

if query:
    with st.spinner("🔍 Thinking..."):
        response = get_deepseek_response(query)
        st.markdown("### 🤖 Bot Response")
        st.markdown(response)

# 🔲 Optional Botpress Visual Embed
st.markdown("---")
st.markdown("### 🔲 Optional Bot UI (for visual embed only)")
st.components.v1.html(
    f"""
    <script src="https://cdn.botpress.cloud/webchat/v3.1/inject.js"></script>
    <div id="webchat" style="width: 100%; height: 500px;"></div>
    <script>
      window.botpressWebChat.init({{
        "botId": "{BOT_ID}",
        "clientId": "{CLIENT_ID}",
        "hostUrl": "https://cdn.botpress.cloud/webchat/v3",
        "messagingUrl": "https://messaging.botpress.cloud",
        "botName": "FPA",
        "composerPlaceholder": "Ask me anything about budgeting or investing...",
        "useSessionStorage": true,
        "disableAnimations": false
      }});
    </script>
    """,
    height=520,
    scrolling=True
)
