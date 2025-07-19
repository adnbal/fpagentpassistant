# budget_invest_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai
import datetime
from botpress_client import BotpressClient

# 🔐 Secrets
CHAT_API_ID = st.secrets["botpress"]["chat_api_id"]  # Used for iframe only
BOTPRESS_TOKEN = st.secrets["botpress"]["token"]
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# 📄 App config
st.set_page_config(page_title="💸 Budgeting + Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (AI Suggestions)")

# 📊 Dummy Forecasting Data
def generate_dummy_returns():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=24, freq="ME")
    dummy_prices = pd.Series(100 + (pd.np.random.randn(len(dates)).cumsum()), index=dates)
    returns = dummy_prices.pct_change().dropna() * 100
    df = pd.DataFrame({"Date": returns.index, "Monthly Return %": returns.values})
    return df

# 🎨 Display forecasting chart
def plot_returns_chart(df):
    fig = px.line(df, x="Date", y="Monthly Return %", title="📈 Dummy Forecasted Returns")
    st.plotly_chart(fig, use_container_width=True)

# 🧠 Gemini suggestion
def get_gemini_suggestion(income, expenses, savings):
    prompt = f"""
    Given the following details:
    - Monthly Income: ${income}
    - Monthly Expenses: ${expenses}
    - Monthly Savings: ${savings}
    Suggest how to improve budgeting and investment.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 📌 Input section
st.subheader("📥 Enter Your Budget Details")
income = st.number_input("Monthly Income ($)", min_value=0)
expenses = st.number_input("Monthly Expenses ($)", min_value=0)
savings = st.number_input("Monthly Savings ($)", min_value=0)
user_input = st.text_input("Ask your Budgeting Assistant (Botpress):")

# 🎯 Analysis section
if income and expenses:
    st.subheader("📊 Budget Summary")
    remaining = income - expenses - savings
    st.write(f"💡 Remaining amount after expenses and savings: ${remaining}")
    if expenses > income * 0.8:
        st.warning("⚠️ Your expenses are more than 80% of your income. Consider reducing them! 💸")
    if savings < income * 0.1:
        st.info("📉 Your savings are below 10% of your income. Try to save more. 🏦")

    # 🌱 Investment Forecast
    st.subheader("🔮 Investment Forecast (Simulated Data)")
    df_returns = generate_dummy_returns()
    plot_returns_chart(df_returns)

    # 🤖 Gemini AI Suggestion
    st.subheader("🧠 Gemini Advice")
    gemini_response = get_gemini_suggestion(income, expenses, savings)
    st.success(gemini_response)

# 💬 Botpress Chat (Button Trigger)
st.subheader("🤖 Chat with Botpress AI")
st.markdown("Ask your Budgeting Assistant (Botpress):")
if st.button("Submit Botpress Query") and user_input:
    client = BotpressClient(api_id=CHAT_API_ID, user_key=BOTPRESS_TOKEN)
    convo = client.create_conversation()
    convo_id = convo.get("id")

    if convo_id:
        client.send_message(convo_id, user_input)
        messages = client.list_messages(convo_id)
        if messages.get("messages"):
            for msg in messages["messages"]:
                text = msg.get("payload", {}).get("text", "")
                if text:
                    st.markdown(f"**Botpress:** {text}")
        else:
            st.warning("⚠️ No response received from Botpress.")
    else:
        st.error("⚠️ Failed to start Botpress conversation.")
