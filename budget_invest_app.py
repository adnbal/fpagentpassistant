import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import requests
from botpress_client import BotpressClient

# 🔐 Secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# 📄 App config
st.set_page_config(page_title="💸 Budget & Investment Planner (Botpress + Gemini + DeepSeek)", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📊 Dummy financial return data (replace Alpha Vantage)
def get_dummy_monthly_return():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
    data = {
        "date": dates,
        "adj_close": [100 + i * 2 + (i % 3 - 1) * 5 for i in range(12)]  # some varied uptrend
    }
    df = pd.DataFrame(data)
    return df

# 📉 Line chart for investment returns
st.subheader("📈 Monthly Investment Return (Dummy Data)")
df = get_dummy_monthly_return()
fig = px.line(df, x="date", y="adj_close", title="Monthly Adjusted Close Price (Synthetic)")
st.plotly_chart(fig, use_container_width=True)

# 💬 Income, Expenses, and Savings Inputs
st.subheader("💰 Enter Your Budget Details")

income = st.number_input("Monthly Income ($)", min_value=0)
expenses = st.number_input("Monthly Expenses ($)", min_value=0)
savings = income - expenses
st.metric("Estimated Monthly Savings", f"${savings:,.2f}")

# ⚠️ Dynamic Warning
if savings < 100:
    st.warning("⚠️ Your savings are low! Consider reducing your expenses.")
elif savings > 1000:
    st.success("🎉 Great! You have strong savings potential.")

# 🤖 Gemini AI: Smart Suggestions
st.subheader("🤖 Gemini Financial Suggestion")

if income > 0 and expenses > 0:
    prompt = f"""You are a financial planner AI. The user has a monthly income of ${income} and monthly expenses of ${expenses}.
    Provide budgeting and investment advice in a friendly tone."""
    gemini_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    st.info(gemini_response.text)

# 📢 DeepSeek AI (via OpenRouter)
st.subheader("🧠 DeepSeek Investment Advice")

if income > 0 and expenses > 0:
    deepseek_prompt = f"""You are an expert investment advisor. The user's income is ${income} and expenses are ${expenses}.
    Give investment suggestions and asset allocation tips."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": deepseek_prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.success(reply)
    else:
        st.error("DeepSeek failed to respond.")

# 💬 Botpress Assistant
st.subheader("😄 Chat with Botpress AI")

query = st.text_input("Ask your Budgeting Assistant (Botpress):")
submit = st.button("Submit")

if submit and query:
    client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
    conv = client.create_conversation()
    conv_id = conv.get("id")
    if conv_id:
        client.send_message(conv_id, query)
        result = client.list_messages(conv_id)
        messages = result.get("messages", [])
        for m in reversed(messages):
            if m["type"] == "text" and m["role"] == "assistant":
                st.markdown(f"**🤖 Botpress Reply:** {m['text']}")
                break
    else:
        st.error("❌ Failed to create Botpress conversation.")
