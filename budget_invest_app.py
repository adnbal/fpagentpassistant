import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 🔐 API keys from Streamlit secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_KEY = st.secrets["alpha_vantage"]["api_key"]

# 🌐 STREAMLIT APP
st.set_page_config(page_title="💸 Budget + Investment Planner (AI)", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 💼 Collect user inputs
income = st.number_input("💰 Monthly Income", value=5000)
expenses = st.number_input("🧾 Monthly Expenses", value=3000)
savings = income - expenses

st.markdown(f"### 🟢 Estimated Savings: **${savings}**")

if savings < 0:
    st.error("⚠️ You're spending more than your income!")
elif savings < 500:
    st.warning("💡 Consider cutting down some expenses to save more.")
else:
    st.success("✅ Good job! You're saving well.")

# 📈 Alpha Vantage Investment Returns
def get_alpha_vantage_monthly_return(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json().get("Monthly Adjusted Time Series", {})
    df = pd.DataFrame.from_dict(data, orient="index")
    df = df.rename(columns={"5. adjusted close": "adjusted_close"})
    df["adjusted_close"] = df["adjusted_close"].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df["monthly_return_%"] = df["adjusted_close"].pct_change() * 100
    return df[["adjusted_close", "monthly_return_%"]]

st.subheader("📊 Investment: S&P 500 (Monthly Returns)")
df_returns = get_alpha_vantage_monthly_return("SPY")
if df_returns is not None:
    st.line_chart(df_returns["monthly_return_%"])
else:
    st.warning("Could not fetch investment data.")

# ✨ AI Suggestion
def get_gemini_reply(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()
    response = chat.send_message(text)
    return response.text

query = st.text_input("🤖 Ask the AI about budgeting or investments")
if query:
    response = get_gemini_reply(query)
    st.markdown("**💬 AI Suggestion:**")
    st.info(response)

# =====================================================================
# 🚀 FASTAPI BACKEND FOR ANDROID VOICE ASSISTANT
# =====================================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/voice")
async def voice_reply(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    ai_reply = get_gemini_reply(user_message)
    return {"reply": ai_reply}

# Optional: Run locally with `uvicorn budget_invest_app:app --reload`
