import streamlit as st
import requests
import google.generativeai as genai

# 🔐 Load secrets
DEEPSEEK_KEY = st.secrets["openrouter"]["api_key"]
GEMINI_KEY = st.secrets["gemini"]["api_key"]
genai.configure(api_key=GEMINI_KEY)

# 🌐 DeepSeek response function
def get_deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-ai/deepseek-chat",  # ✅ CORRECTED model ID
        "messages": [
            {"role": "system", "content": "You are a financial assistant. Provide helpful budgeting and investment advice."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        else:
            return f"⚠️ Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# ✨ Streamlit UI
st.set_page_config(page_title="💬 Budgeting Chat Assistant", layout="centered")
st.title("💬 Budgeting Chat Assistant")
st.markdown("Ask anything about your **income**, **expenses**, or **investments** below.")

# 📝 User input
user_input = st.text_input("Type your question for the bot:")

# 💬 Show reply
if user_input:
    with st.spinner("Talking to DeepSeek..."):
        response = get_deepseek_response(user_input)
    st.markdown(f"**Bot Response:** {response}")
