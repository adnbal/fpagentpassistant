import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="AI Investment Advisor", page_icon=":moneybag:")

st.title("🤖💰 AI Investment Advisor")
st.write(
    "Plan your investments and get AI-powered advice. "
    "All computations are for educational purposes only."
)

# --- INPUTS ---
st.sidebar.header("Investor Profile")
age = st.sidebar.number_input("Your Age", min_value=18, max_value=100, value=30)
goal = st.sidebar.text_area("Investment Goal", "Retire early with financial security")
initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=1000, max_value=1_000_000, value=10_000, step=1000)
years = st.sidebar.slider("Investment Duration (Years)", 1, 40, 10)
annual_contribution = st.sidebar.number_input("Annual Contribution ($)", min_value=0, max_value=100_000, value=0, step=500)
risk_profile = st.sidebar.selectbox("Risk Profile", ["Conservative", "Balanced", "Aggressive"])

# --- PROJECTIONS ---
risk_params = {
    "Conservative": (0.04, 0.02),   # (avg return, std dev)
    "Balanced": (0.07, 0.05),
    "Aggressive": (0.10, 0.10),
}
exp_return, std_dev = risk_params[risk_profile]
st.write(f"**Risk Profile:** {risk_profile} — Expected annual return: {exp_return*100:.1f}%, Volatility: {std_dev*100:.1f}%")

# Simulate investment growth
np.random.seed(1)
years_range = np.arange(1, years+1)
portfolio = [initial_investment]
for i in range(1, years+1):
    growth = portfolio[-1]*(1 + np.random.normal(exp_return, std_dev))
    growth += annual_contribution
    portfolio.append(growth)
df = pd.DataFrame({'Year': np.arange(0, years+1), 'Portfolio Value': portfolio})

st.subheader("Projected Portfolio Growth")
st.line_chart(df.set_index('Year'))

# Asset allocation suggestion
allocations = {
    "Conservative": {"Bonds": 70, "Stocks": 25, "Real Estate": 5},
    "Balanced": {"Bonds": 40, "Stocks": 55, "Real Estate": 5},
    "Aggressive": {"Bonds": 10, "Stocks": 85, "Real Estate": 5}
}
st.subheader("Suggested Asset Allocation")
st.write(allocations[risk_profile])
fig, ax = plt.subplots()
ax.pie(list(allocations[risk_profile].values()), labels=allocations[risk_profile].keys(), autopct='%1.1f%%')
st.pyplot(fig)

st.subheader("Download Your Projection")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", data=csv, file_name='investment_projection.csv', mime='text/csv')

st.info("**Note:** This app is for educational purposes. Actual investment outcomes may vary.")

# --- AI ADVISOR ---
st.header("Ask the AI Investment Advisor")
st.markdown("_Powered by OpenAI GPT-4. Your API key is securely managed by Streamlit Cloud secrets._")

user_question = st.text_area(
    "What would you like to ask the AI advisor?",
    "How should I invest for my goal?"
)

if st.button("Ask AI Advisor"):
    # Retrieve OpenAI API key from Streamlit secrets
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OpenAI API key not found in Streamlit secrets. Please configure secrets in Streamlit Cloud.")
    elif not user_question.strip():
        st.warning("Please enter a question for the AI advisor.")
    else:
        with st.spinner("AI is analyzing your profile and question..."):
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            prompt = (
                f"You are a financial advisor AI. The user is {age} years old, wants to '{goal}', "
                f"has ${initial_investment} to invest, {years} year horizon, "
                f"annual contribution of ${annual_contribution}, "
                f"and a {risk_profile} risk profile. "
                f"User asks: {user_question}\n"
                "Give a detailed, actionable answer in plain English. Do not give tax or legal advice."
            )
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful investment advisor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )
                st.success(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"OpenAI API error: {e}")

st.markdown("> **Disclaimer:** This app provides general information only. Not financial advice.")

st.subheader("💡 Smart Investing Tips")
st.markdown("""
- Diversify your portfolio to manage risk.
- Review your investments periodically.
- Consider dollar-cost averaging.
- Reinvest dividends for compounding.
- Invest for the long term and avoid emotional decisions.
""")
