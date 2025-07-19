import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai
import openai
import json
from botpress_client import BotpressClient

# 🔐 Load secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
ALPHA_VANTAGE_API_KEY = st.secrets["alpha_vantage"]["api_key"]

# 📄 Streamlit setup
st.set_page_config(page_title="💸 Multi-LLM Budget Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 🧾 Collect budget inputs
income = st.number_input("Monthly Income", min_value=0)
expenses = st.number_input("Monthly Expenses", min_value=0)
savings = st.number_input("Current Savings", min_value=0)

# 📊 Pie Chart
if income > 0:
    data = pd.DataFrame({
        "Category": ["Expenses", "Savings", "Remaining"],
        "Amount": [expenses, savings, income - expenses - savings]
    })
    fig = px.pie(data, values="Amount", names="Category", title="💰 Budget Distribution")
    st.plotly_chart(fig)

# ⚠️ Dynamic Warnings
warnings = []
if expenses > income * 0.7:
    warnings.append("⚠️ Your expenses exceed 70% of income. Reduce discretionary spending.")
if savings < income * 0.2:
    warnings.append("💡 Consider increasing your savings to at least 20% of income.")
if income - expenses - savings < 0:
    warnings.append("🚨 Your spending exceeds income. Adjust budget to avoid debt.")

if warnings:
    st.subheader("📌 Financial Warnings")
    for w in warnings:
        st.warning(w)

# 📈 Alpha Vantage investment data
def get_alpha_vantage_monthly_return(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    ts = data.get("Monthly Adjusted Time Series", {})
    df = pd.DataFrame(ts).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df["adj_close"] = pd.to_numeric(df["5. adjusted close"], errors="coerce")
    df["monthly_return"] = df["adj_close"].pct_change()
    return df[["adj_close", "monthly_return"]].dropna()

# 📉 Show investment returns
with st.expander("📈 Investment Option Analysis (S&P 500)"):
    df = get_alpha_vantage_monthly_return("SPY")
    if df is not None:
        st.line_chart(df["adj_close"])
        st.line_chart(df["monthly_return"])
    else:
        st.error("Failed to fetch Alpha Vantage data.")

# 🧠 Gemini Suggestions
def gemini_budget_advice(income, expenses, savings):
    prompt = f"""My monthly income is {income}, expenses are {expenses}, and current savings are {savings}.
    Give personalized budgeting and investment suggestions in bullet points."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 🧠 DeepSeek (OpenRouter) Suggestions
def deepseek_advice(income, expenses, savings):
    prompt = f"""You are a financial assistant. User earns {income}, spends {expenses}, and has {savings} in savings.
Provide budgeting and investment advice."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    try:
        return res.json()["choices"][0]["message"]["content"]
    except:
        return "DeepSeek failed."

# 🔮 LLM Advice
st.subheader("🔮 AI-Based Financial Suggestions")
tab1, tab2 = st.tabs(["Gemini Advice", "DeepSeek Advice"])
with tab1:
    st.markdown(gemini_budget_advice(income, expenses, savings))
with tab2:
    st.markdown(deepseek_advice(income, expenses, savings))

# 💬 Botpress Chat
st.subheader("🤖 Chat With Your AI Assistant")
with st.container():
    st.components.v1.iframe(
        f"https://chat.botpress.cloud/embed?botId={CHAT_API_ID}",
        height=500,
        scrolling=True
    )
