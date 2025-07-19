import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import google.generativeai as genai

# 🔐 Secrets
BOT_ID = st.secrets["botpress"]["bot_id"]
CLIENT_ID = st.secrets["botpress"]["client_id"]
TOKEN = st.secrets["botpress"]["token"]
GEMINI_KEY = st.secrets["gemini"]["api_key"]
DEEPSEEK_KEY = st.secrets["openrouter"]["api_key"]

# 🌐 Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# 📄 App config
st.set_page_config(page_title="💸 Budgeting + Investment Planner", layout="wide")
st.title("💸 Budgeting + Investment Planner (Multi-LLM AI Suggestions)")

# 📊 Sidebar Inputs
st.sidebar.header("📊 Monthly Income")
income = st.sidebar.number_input("Monthly income (before tax, $)", min_value=0.0, value=5000.0, step=100.0)
tax_rate = st.sidebar.slider("Tax rate (%)", 0, 50, 20)

st.sidebar.header("📌 Expenses")
housing = st.sidebar.number_input("Housing / Rent ($)", 0.0, 5000.0, 1200.0, 50.0)
food = st.sidebar.number_input("Food / Groceries ($)", 0.0, 5000.0, 500.0, 50.0)
transport = st.sidebar.number_input("Transport ($)", 0.0, 5000.0, 300.0, 50.0)
utilities = st.sidebar.number_input("Utilities ($)", 0.0, 5000.0, 200.0, 50.0)
entertainment = st.sidebar.number_input("Entertainment ($)", 0.0, 5000.0, 200.0, 50.0)
others = st.sidebar.number_input("Other expenses ($)", 0.0, 5000.0, 200.0, 50.0)

st.sidebar.header("📈 Investments")
stocks = st.sidebar.number_input("Stocks investment ($)", 0.0, 5000.0, 500.0, 100.0)
bonds = st.sidebar.number_input("Bonds investment ($)", 0.0, 5000.0, 300.0, 100.0)
real_estate = st.sidebar.number_input("Real estate ($)", 0.0, 5000.0, 0.0, 100.0)
crypto = st.sidebar.number_input("Crypto ($)", 0.0, 5000.0, 0.0, 100.0)
fixed_deposit = st.sidebar.number_input("Fixed deposit ($)", 0.0, 5000.0, 0.0, 100.0)

months = st.sidebar.slider("Projection period (months)", 1, 60, 12)
savings_target = st.sidebar.number_input("Savings target at end of period ($)", 0.0, 1_000_000.0, 10000.0, 500.0)

# 🧮 Calculations
after_tax_income = income * (1 - tax_rate / 100)
total_exp = housing + food + transport + utilities + entertainment + others
total_inv = stocks + bonds + real_estate + crypto + fixed_deposit
net_flow = after_tax_income - total_exp - total_inv

# Dummy returns
stock_r, bond_r, real_r, crypto_r, fd_r = 0.01, 0.003, 0.004, 0.02, 0.003

bal = 0
rows = []
for m in range(1, months + 1):
    bal += net_flow
    stock_val = stocks * ((1 + stock_r)**m - 1) / stock_r
    bond_val = bonds * ((1 + bond_r)**m - 1) / bond_r
    real_val = real_estate * ((1 + real_r)**m - 1) / real_r
    crypto_val = crypto * ((1 + crypto_r)**m - 1) / crypto_r
    fd_val = fixed_deposit * ((1 + fd_r)**m - 1) / fd_r
    net_worth = bal + stock_val + bond_val + real_val + crypto_val + fd_val
    rows.append({
        "Month": m,
        "Balance": bal,
        "Stocks": stock_val,
        "Bonds": bond_val,
        "RealEstate": real_val,
        "Crypto": crypto_val,
        "FixedDeposit": fd_val,
        "NetWorth": net_worth
    })
df = pd.DataFrame(rows)

# 📋 Summary
st.subheader("📋 Summary")
st.metric("After tax income", f"${after_tax_income:,.2f}")
st.metric("Expenses", f"${total_exp:,.2f}")
st.metric("Investments", f"${total_inv:,.2f}")
st.metric("Net Cash Flow", f"${net_flow:,.2f}/mo")

# 📈 Graphs
st.subheader("📈 Net Worth Growth")
fig = px.line(df, x="Month", y=["Balance", "Stocks", "Bonds", "RealEstate", "Crypto", "FixedDeposit", "NetWorth"],
              markers=True, title="Net Worth & Investments Over Time")
fig.add_hline(y=savings_target, line_dash="dash", line_color="red", annotation_text="Target")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🧾 Expense Breakdown")
exp_s = pd.Series({
    "Housing": housing, "Food": food, "Transport": transport,
    "Utilities": utilities, "Entertainment": entertainment, "Others": others
})
st.plotly_chart(px.pie(names=exp_s.index, values=exp_s.values, title="Expense Breakdown"), use_container_width=True)

st.subheader("💼 Investment Breakdown")
inv_s = pd.Series({
    "Stocks": stocks, "Bonds": bonds, "RealEstate": real_estate,
    "Crypto": crypto, "FixedDeposit": fixed_deposit
})
st.plotly_chart(px.pie(names=inv_s.index, values=inv_s.values, title="Investment Breakdown"), use_container_width=True)

# 🧠 AI Prompt
prompt = f"""
Financial Summary:
Gross Income: ${income}
Tax Rate: {tax_rate}%
After-tax Income: ${after_tax_income}
Expenses: ${total_exp}
Investments: ${total_inv}
Net cash flow: ${net_flow}/mo
Savings Target: ${savings_target}
Projected Net Worth: ${df['NetWorth'].iloc[-1]}

Provide personalized advice on spending control, investment strategy, and how to reach the savings target.
"""

# 🤖 AI Outputs
st.subheader("🤖 AI Suggestions")
col1, col2 = st.columns(2)

if col1.button("💡 Gemini Suggestion"):
    with st.spinner("Thinking..."):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini error: {e}")

if col2.button("🧠 DeepSeek Suggestion"):
    with st.spinner("Thinking..."):
        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {"role": "system", "content": "You are a budgeting assistant. Provide concise financial advice."},
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            reply = res.json()['choices'][0]['message']['content']
            st.write(reply)
        except Exception as e:
            st.error(f"OpenRouter error: {e}")

# 💬 Chat Assistant (Botpress iframe)
st.subheader("💬 Ask Your Financial Assistant")
iframe_url = "https://cdn.botpress.cloud/webchat/v3.0/shareable.html?configUrl=https://files.bpcontent.cloud/2025/07/02/02/20250702020605-VDMFG1YB.json"
st.markdown(f"""
<iframe src="{iframe_url}" width="100%" height="600" style="border: none; margin-top: 20px;" allow="microphone"></iframe>
""", unsafe_allow_html=True)
