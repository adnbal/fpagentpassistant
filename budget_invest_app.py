import streamlit as st
import pandas as pd
import plotly.express as px
import random
import google.generativeai as genai
from botpress_client import BotpressClient
import requests
import datetime

# 🔐 Load secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
GENAI_KEY = st.secrets["gemini"]["api_key"]
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

genai.configure(api_key=GENAI_KEY)

# 🌐 Botpress Client setup
client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
if "conversation_id" not in st.session_state:
    convo = client.create_conversation()
    st.session_state.conversation_id = convo.get("id", "")

# 🎨 App UI
st.set_page_config(page_title="💸 Budgeting & Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📥 Input Section
income = st.number_input("Monthly Income (NZD)", min_value=0)
expenses = st.number_input("Monthly Expenses (NZD)", min_value=0)
savings = income - expenses

# ⚠️ Warnings
if income == 0:
    st.warning("⚠️ Please enter your income.")
elif expenses > income:
    st.error("🚨 Your expenses exceed your income!")
elif savings < income * 0.2:
    st.warning("⚠️ Try to save at least 20% of your income.")
else:
    st.success("✅ Good budgeting! You're saving enough. 💰")

# 📊 Forecasting using dummy values
def dummy_forecast():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
    return pd.DataFrame({
        "date": dates,
        "projected_savings": [savings + random.randint(-100, 300) for _ in range(12)]
    })

forecast_df = dummy_forecast()
st.subheader("📈 Savings Forecast (Next 12 Months)")
fig = px.line(forecast_df, x="date", y="projected_savings", title="Projected Savings Over Time")
st.plotly_chart(fig, use_container_width=True)

# 🤖 Gemini Suggestions
if income > 0 and expenses > 0:
    gemini_prompt = f"My income is {income} NZD and expenses are {expenses} NZD. Give budgeting and investment advice."
    model = genai.GenerativeModel("gemini-1.5-flash")
    gemini_reply = model.generate_content(gemini_prompt)
    st.subheader("🧠 Gemini Advice")
    st.info(gemini_reply.text)

# 🧠 DeepSeek (OpenRouter) Suggestion
import openai
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

if income > 0 and expenses > 0:
    deepseek_prompt = f"My income is {income} NZD and expenses are {expenses} NZD. What should I do to improve budgeting and grow wealth?"
    try:
        response = openai.ChatCompletion.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": deepseek_prompt}]
        )
        deepseek_reply = response.choices[0].message.content
        st.subheader("🔍 DeepSeek Advice")
        st.info(deepseek_reply)
    except Exception as e:
        st.warning(f"DeepSeek error: {e}")

# 💬 Botpress Chat
st.subheader("💬 Ask your Budgeting Assistant (Botpress):")
query = st.text_input("Type your question for Botpress")
if st.button("Submit") and query:
    client.send_message(st.session_state.conversation_id, query)
    messages = client.list_messages(st.session_state.conversation_id)
    if messages and "messages" in messages and messages["messages"]:
        last_reply = messages["messages"][-1]["payload"].get("text", "⚠️ No message content.")
        st.success(last_reply)
    else:
        st.error("⚠️ No response received from Botpress.")

# 🧾 Footer
st.markdown("---")
st.markdown("Made with 💡 by your AI financial planner.")
