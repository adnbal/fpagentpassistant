import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai
import time

# 🔐 Load secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
ALPHA_API_KEY = st.secrets["alpha_vantage"]["api_key"]

# 📄 Page config
st.set_page_config(page_title="💸 Budgeting & Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📥 Collect inputs
income = st.number_input("💰 Enter your monthly income", value=5000)
expenses = st.number_input("📤 Enter your monthly expenses", value=3000)
savings = st.number_input("🏦 Current savings", value=10000)

st.divider()

# 📊 Pie Chart
df = pd.DataFrame({
    'Category': ['Expenses', 'Remaining'],
    'Amount': [expenses, income - expenses]
})
fig = px.pie(df, names='Category', values='Amount', title='💸 Expense Breakdown')
st.plotly_chart(fig, use_container_width=True)

# ⚠️ Dynamic warnings
if expenses > income:
    st.warning("🚨 You are spending more than you earn! Cut down on non-essential expenses.")
elif expenses > 0.8 * income:
    st.info("🔎 Your expenses are above 80% of income. Review spending habits.")
else:
    st.success("✅ Your spending is within a healthy range.")

# 🧠 Gemini investment advice
prompt = f"""
My income is {income}, expenses are {expenses}, and I have {savings} in savings.
Give budgeting and investment suggestions.
"""

if st.button("🧠 Get Gemini Advice"):
    with st.spinner("Gemini thinking..."):
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        st.subheader("💡 Gemini Suggests:")
        st.markdown(response.text)

# 🧠 DeepSeek investment advice
if st.button("🔍 Get DeepSeek Advice"):
    with st.spinner("DeepSeek analyzing..."):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a budgeting and investment expert."},
                {"role": "user", "content": prompt}
            ]
        }
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            deepseek_text = res.json()["choices"][0]["message"]["content"]
            st.subheader("💡 DeepSeek Suggests:")
            st.markdown(deepseek_text)
        else:
            st.error("⚠️ DeepSeek failed to respond. Check API key or usage.")

st.divider()

# 📈 Optional: Alpha Vantage returns
def get_alpha_vantage_monthly_return(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={ALPHA_API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    try:
        ts = r.json()["Monthly Adjusted Time Series"]
        df = pd.DataFrame.from_dict(ts, orient='index')
        df = df.astype(float)
        df['return'] = df['5. adjusted close'].pct_change()
        return df[['5. adjusted close', 'return']].dropna().head(12)
    except:
        return None

st.subheader("📊 Sample Investment Returns (Alpha Vantage)")
symbol = st.text_input("Enter a stock symbol (e.g. AAPL, MSFT)", value="AAPL")
if symbol:
    df_ret = get_alpha_vantage_monthly_return(symbol)
    if df_ret is not None:
        st.line_chart(df_ret['5. adjusted close'])
    else:
        st.warning("No data found or API limit reached.")

# 💬 Embedded Botpress assistant
st.subheader("💬 Talk to Your Budget Bot")
st.components.v1.html(
    f"""
    <iframe
        src="https://chat.botpress.cloud/{CHAT_API_ID}/webchat"
        width="100%" height="600" frameborder="0"
    ></iframe>
    """,
    height=620
)
