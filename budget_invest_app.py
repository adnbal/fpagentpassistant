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
API_KEY = st.secrets.get("alpha_vantage", {}).get("api_key", "")

# 📄 App config
st.set_page_config(page_title="💸 Budget & Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 🎯 Try fetching data from Alpha Vantage, else fallback
@st.cache_data
def get_alpha_vantage_monthly_return(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
        r = requests.get(url)
        data = r.json()
        ts = data.get("Monthly Adjusted Time Series", {})
        if not ts:
            raise ValueError("Alpha Vantage returned no data.")
        df = pd.DataFrame.from_dict(ts, orient="index")
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df["adj_close"] = pd.to_numeric(df["5. adjusted close"], errors="coerce")
        df = df[["adj_close"]].dropna()
        return df.tail(12)
    except Exception as e:
        st.warning("📉 Could not fetch from Alpha Vantage. Using dummy returns.")
        dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
        returns = [100 + i * 2 + (i % 3) * 5 for i in range(12)]
        df = pd.DataFrame({"adj_close": returns}, index=dates)
        return df

# 📊 Display past returns
st.subheader("📈 Investment Trend: SPY (or Simulated)")
df = get_alpha_vantage_monthly_return("SPY")
st.line_chart(df)

# 🧾 Input
income = st.number_input("Monthly Income", min_value=0)
expenses = st.number_input("Monthly Expenses", min_value=0)
savings = st.number_input("Monthly Savings", min_value=0)

# ⚠️ Warnings
if expenses > income:
    st.error("🚨 Your expenses are greater than your income!")
elif savings < income * 0.2:
    st.warning("💡 You are saving less than 20% of your income. Consider reducing expenses.")
else:
    st.success("✅ Your budgeting looks healthy!")

# 💡 Gemini Investment Advice
if st.button("Ask Gemini for Investment Suggestions"):
    prompt = f"My income is {income}, expenses are {expenses}, savings {savings}. Give investment advice."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    st.markdown("### 🧠 Gemini's Suggestions:")
    st.info(response.text)

# 💬 Botpress Chat Assistant
st.subheader("🤖 Chat with Botpress AI")

query = st.text_input("Ask your Budgeting Assistant (Botpress):", key="user_query")
if query:
    client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
    conv = client.create_conversation()
    conv_id = conv.get("id")
    if conv_id:
        client.send_message(conv_id, query)
        result = client.list_messages(conv_id)
        messages = result.get("messages", [])
        for m in reversed(messages):
            if m["type"] == "text" and m["role"] == "assistant":
                st.success(m["text"])
                break
    else:
        st.error("❌ Failed to connect to Botpress.")
