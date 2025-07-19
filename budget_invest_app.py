# budget_invest_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai
from botpress_client import BotpressClient  # ✅ This uses the updated BotpressClient

# 🔐 Load Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]
GEMINI_KEY = st.secrets["gemini"]["api_key"]
DEEPSEEK_KEY = st.secrets["openrouter"]["api_key"]

# 📄 App Config
st.set_page_config(page_title="💸 Budgeting + Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📊 Budget Input Section
st.header("📥 Enter Your Budget Details")

income = st.number_input("Monthly Income ($)", min_value=0)
expenses = st.number_input("Monthly Expenses ($)", min_value=0)
savings = st.number_input("Current Savings ($)", min_value=0)

# 🧠 Warnings
st.subheader("⚠️ AI Financial Warnings")
if expenses > income:
    st.error("🚨 You're spending more than you earn!")
elif expenses > 0.8 * income:
    st.warning("⚠️ High expenses — consider reducing discretionary spending.")
else:
    st.success("✅ Your budget looks healthy!")

# 📈 Pie Chart
st.subheader("📊 Budget Allocation")
budget_data = pd.DataFrame({
    'Category': ['Income', 'Expenses', 'Savings'],
    'Amount': [income, expenses, savings]
})
fig = px.pie(budget_data, names='Category', values='Amount', title='Budget Distribution')
st.plotly_chart(fig, use_container_width=True)

# 🤖 Gemini Suggestion
st.subheader("📢 Gemini AI Investment Advice")
genai.configure(api_key=GEMINI_KEY)

def get_gemini_advice(income, expenses, savings):
    prompt = f"""
    I have a monthly income of ${income}, expenses of ${expenses}, and savings of ${savings}.
    Provide 3 short investment suggestions tailored for my situation.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

if income > 0:
    advice = get_gemini_advice(income, expenses, savings)
    st.info(advice)

# 💬 Ask a Question via Botpress
st.subheader("💬 Budgeting Chat Assistant")
user_input = st.text_input("Type your question for the bot:")

if st.button("Submit") and user_input:
    try:
        # 🟢 Set up Botpress Client
        bp_client = BotpressClient(BOT_ID, CLIENT_ID, TOKEN)

        # 🟢 Create conversation and send message
        conversation_id = bp_client.create_conversation()
        bp_client.send_message(conversation_id, user_input)
        messages = bp_client.list_messages(conversation_id)

        if messages:
            last_msg = messages[-1].get("payload", {}).get("text", "No message returned.")
            st.success(f"🤖 Botpress: {last_msg}")
        else:
            st.warning("⚠️ No messages returned from Botpress.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
