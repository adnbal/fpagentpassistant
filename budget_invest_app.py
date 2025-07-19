import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai

# 🔐 Secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_KEY = st.secrets["alpha_vantage"]["api_key"]

# 📄 App config
st.set_page_config(page_title="💸 Multi-LLM Budget Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📉 Alpha Vantage return function
def get_alpha_vantage_monthly_return(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        st.error("Failed to fetch data from Alpha Vantage.")
        return None

    data = r.json()
    if "Monthly Adjusted Time Series" not in data:
        st.error("Alpha Vantage API response is missing expected data.")
        return None

    ts = data["Monthly Adjusted Time Series"]
    df = pd.DataFrame.from_dict(ts, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    if "5. adjusted close" not in df.columns:
        st.error("Missing '5. adjusted close' in Alpha Vantage response.")
        return None

    df["adjusted_close"] = df["5. adjusted close"].astype(float)
    df["monthly_return"] = df["adjusted_close"].pct_change()

    return df[["adjusted_close", "monthly_return"]].dropna()

# 📊 Investment section
st.subheader("📈 SPY Monthly Returns from Alpha Vantage")
df_returns = get_alpha_vantage_monthly_return("SPY")
if df_returns is not None:
    st.line_chart(df_returns["adjusted_close"], use_container_width=True)
    st.bar_chart(df_returns["monthly_return"], use_container_width=True)

# 💰 User budget input
st.subheader("🧾 Enter Your Budget Details")
income = st.number_input("Monthly Income", min_value=0)
expenses = st.number_input("Monthly Expenses", min_value=0)
savings = st.number_input("Target Savings", min_value=0)

# 🚨 Warnings
if income > 0:
    if expenses > income:
        st.warning("⚠️ Your expenses exceed your income. Consider reducing discretionary spending.")
    elif savings > (income - expenses):
        st.warning("⚠️ Your savings target is more than your leftover income. Adjust your plan.")
    else:
        st.success("✅ Your budgeting plan looks healthy!")

# 🤖 Gemini AI advice
if income > 0 and expenses > 0:
    prompt = f"My income is ${income}, expenses are ${expenses}, and I want to save ${savings} monthly. Give personalized budgeting and investment advice."
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    st.subheader("🤖 Gemini Financial Advisor")
    st.markdown(response.text)

# 🤖 DeepSeek AI investment ideas (via OpenRouter)
import openai
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

if income > 0 and expenses > 0:
    st.subheader("💡 DeepSeek Investment Insights")
    try:
        completion = openai.ChatCompletion.create(
            model="deepseek/deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a smart investment advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        deepseek_reply = completion.choices[0].message.content
        st.markdown(deepseek_reply)
    except Exception as e:
        st.error(f"DeepSeek error: {e}")

# 💬 Embedded Botpress assistant
st.subheader("🧠 Ask the Budgeting Bot")
st.components.v1.iframe(
    f"https://chat.botpress.cloud/{CHAT_API_ID}",
    height=500,
    scrolling=True
)
