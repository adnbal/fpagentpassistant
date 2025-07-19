import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import datetime
from botpress_client import BotpressClient

# 🔐 Load secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]

# 📄 Page Config
st.set_page_config(page_title="💸 Multi-LLM Budget Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📊 Input Form
with st.sidebar.form("budget_form"):
    st.subheader("Enter Your Monthly Budget Details")
    income = st.number_input("Monthly Income", value=5000)
    expenses = st.number_input("Monthly Expenses", value=3000)
    savings = st.number_input("Current Savings", value=10000)
    submitted = st.form_submit_button("Submit")

# ⚠️ Warnings & Suggestions
if submitted:
    st.subheader("📌 Insights & Warnings")

    if expenses > income:
        st.error("🚨 You are spending more than your income! Consider cutting down expenses.")
    elif expenses > 0.8 * income:
        st.warning("⚠️ Your expenses are over 80% of your income. Try to save more.")
    else:
        st.success("✅ Good job! You're managing expenses well.")

    st.info(f"💡 Savings Rate: {round((income - expenses) / income * 100, 2)}%")

    # Dummy Investment Forecast (replace Alpha Vantage)
    st.subheader("📈 Investment Forecast (Dummy)")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=24, freq="ME")
    prices = [100 + i * 2 + (i % 5) * 1.5 for i in range(24)]
    df = pd.DataFrame({"date": dates, "adj_close": prices})
    fig = px.line(df, x="date", y="adj_close", title="Simulated Investment Growth (e.g., SPY ETF)")
    st.plotly_chart(fig, use_container_width=True)

# 🤖 Gemini Suggestion
st.subheader("🤖 Gemini Advice")
if submitted:
    prompt = f"My monthly income is {income}, expenses are {expenses}, and I have savings of {savings}. Provide financial advice."
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    st.write(response.text)

# 🧠 DeepSeek Agent Suggestion
st.subheader("🧠 DeepSeek Advice")
if submitted:
    import requests
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://pafadvisor.streamlit.app/",
        "X-Title": "Budgeting Assistant"
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": f"My income is {income}, expenses {expenses}, savings {savings}. Suggest investment plan."}
        ]
    }
    r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    reply = r.json()["choices"][0]["message"]["content"]
    st.write(reply)

# 💬 Chat with Botpress
st.subheader("😎 Chat with Botpress AI")
st.markdown("Ask your Budgeting Assistant (Botpress):")

# Chat form
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("Your message:", key="chat_input")
    chat_submit = st.form_submit_button("Submit")

# Botpress session and logic
if "conversation_id" not in st.session_state:
    client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
    conv = client.create_conversation()
    st.session_state.conversation_id = conv.get("id")

if chat_submit and user_query:
    client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
    client.send_message(st.session_state.conversation_id, user_query)
    messages = client.list_messages(st.session_state.conversation_id)

    if messages and "messages" in messages:
        replies = [m["text"] for m in messages["messages"] if m["role"] == "assistant" and m["type"] == "text"]
        if replies:
            st.success(f"💬 Botpress: {replies[-1]}")
        else:
            st.warning("Botpress did not reply.")
    else:
        st.error("⚠️ Failed to retrieve messages.")
